# 智选电商平台数据库架构设计 (PostgreSQL主从复制)

## 数据库架构概述

智选电商平台采用PostgreSQL作为主要数据库，通过主从复制实现高可用性和读写分离，满足百万级用户和高并发访问的需求。

## 数据库分库分表策略

### 1. 垂直分库
根据业务领域将数据拆分到不同的数据库：

```
用户数据库 (zhi_xuan_user)
├── users (用户表)
├── user_profiles (用户资料表)
└── user_addresses (用户地址表)

商品数据库 (zhi_xuan_product)
├── products (商品表)
├── categories (分类表)
├── product_images (商品图片表)
└── product_reviews (商品评价表)

订单数据库 (zhi_xuan_order)
├── orders (订单表)
├── order_items (订单项表)
├── order_payments (订单支付表)
└── order_status_history (订单状态历史表)

库存数据库 (zhi_xuan_inventory)
├── inventory (库存表)
├── inventory_logs (库存日志表)
└── warehouses (仓库表)

营销数据库 (zhi_xuan_marketing)
├── coupons (优惠券表)
├── campaigns (营销活动表)
└── user_coupons (用户优惠券表)
```

### 2. 水平分表

对大数据量表进行水平分表：

```sql
-- 订单表按时间分表
CREATE TABLE orders_2023_11 (
    LIKE orders INCLUDING ALL
) INHERITS (orders);

CREATE TABLE orders_2023_12 (
    LIKE orders INCLUDING ALL
) INHERITS (orders);

-- 用户表按用户ID哈希分表
CREATE TABLE users_0 (
    LIKE users INCLUDING ALL
) INHERITS (users);

CREATE TABLE users_1 (
    LIKE users INCLUDING ALL
) INHERITS (users);

-- 分表策略函数
CREATE OR REPLACE FUNCTION get_user_shard(user_id INTEGER)
RETURNS INTEGER AS $$
BEGIN
    RETURN user_id % 4;
END;
$$ LANGUAGE plpgsql;
```

## PostgreSQL主从复制架构

### 主从复制拓扑
```
                    Master (写入) - 高配服务器
                         │
        ┌────────────────┼────────────────┐
        │                │                │
  Slave-Read-1      Slave-Read-2      Slave-Read-3
   (北京机房)        (上海机房)        (深圳机房)
     高可用读        高可用读           灾备+读
```

### 主从复制配置

#### 1. 主库配置 (postgresql.conf)
```conf
# 连接设置
max_connections = 500
superuser_reserved_connections = 10

# WAL设置
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10
wal_keep_size = 512MB
archive_mode = on
archive_command = 'cp %p /var/lib/postgresql/archive/%f'

# 主从同步设置
synchronous_commit = on
synchronous_standby_names = 'standby1'  # 同步复制，确保数据一致性

# 检查点设置
checkpoint_completion_target = 0.9
checkpoint_timeout = 15min
max_wal_size = 4GB
min_wal_size = 1GB

# 性能优化
shared_buffers = 4GB
effective_cache_size = 16GB
work_mem = 32MB
maintenance_work_mem = 512MB
random_page_cost = 1.1
effective_io_concurrency = 200

# 日志设置
log_statement = 'all'
log_min_duration_statement = 1000
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
```

#### 2. 从库配置 (postgresql.conf)
```conf
# 基本配置
max_connections = 300
shared_buffers = 2GB
effective_cache_size = 8GB

# 恢复设置
hot_standby = on
max_standby_streaming_delay = 30s
max_standby_archive_delay = 30s
wal_receiver_status_interval = 10s
hot_standby_feedback = on

# 日志设置
log_min_messages = info
log_error_verbosity = default
```

#### 3. 主库pg_hba.conf配置
```conf
# 允许从库复制连接
host    replication     replicator      10.0.1.0/24         md5
host    replication     replicator      10.0.2.0/24         md5
host    replication     replicator      10.0.3.0/24         md5

# 允许应用连接
host    all             all             0.0.0.0/0           md5
host    all             all             ::0/0               md5
```

## 数据库初始化脚本

### 1. 用户数据库初始化 (zhi_xuan_user)
```sql
-- 创建数据库
CREATE DATABASE zhi_xuan_user WITH 
    OWNER = user_owner
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

\c zhi_xuan_user;

-- 创建扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- 用于模糊搜索优化
CREATE EXTENSION IF NOT EXISTS btree_gin; -- 用于索引优化

-- 用户表
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    status SMALLINT DEFAULT 1, -- 1:正常, 0:禁用
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 用户资料表
CREATE TABLE user_profiles (
    profile_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    nickname VARCHAR(50),
    avatar_url VARCHAR(255),
    gender SMALLINT, -- 0:未知, 1:男, 2:女
    birth_date DATE,
    real_name VARCHAR(50),
    id_card VARCHAR(18),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 用户地址表
CREATE TABLE user_addresses (
    address_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    receiver_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    province VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    district VARCHAR(50) NOT NULL,
    detail_address TEXT NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_user_addresses_user_id ON user_addresses(user_id);
CREATE INDEX idx_user_addresses_is_default ON user_addresses(is_default);

-- 创建更新时间触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at 
    BEFORE UPDATE ON user_profiles 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_addresses_updated_at 
    BEFORE UPDATE ON user_addresses 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### 2. 商品数据库初始化 (zhi_xuan_product)
```sql
-- 创建数据库
CREATE DATABASE zhi_xuan_product WITH 
    OWNER = product_owner
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

\c zhi_xuan_product;

-- 创建扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS btree_gin;

-- 商品分类表
CREATE TABLE categories (
    category_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    parent_id UUID REFERENCES categories(category_id),
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    image_url VARCHAR(255),
    sort_order INTEGER DEFAULT 0,
    status SMALLINT DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 商品表
CREATE TABLE products (
    product_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(200) NOT NULL,
    description TEXT,
    category_id UUID NOT NULL REFERENCES categories(category_id),
    brand VARCHAR(100),
    price DECIMAL(10,2) NOT NULL,
    original_price DECIMAL(10,2),
    stock_quantity INTEGER DEFAULT 0,
    sold_count INTEGER DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 0.00,
    review_count INTEGER DEFAULT 0,
    status SMALLINT DEFAULT 1, -- 1:上架, 0:下架
    is_hot BOOLEAN DEFAULT FALSE,
    is_new BOOLEAN DEFAULT FALSE,
    is_recommend BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 商品图片表
CREATE TABLE product_images (
    image_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    image_url VARCHAR(255) NOT NULL,
    sort_order INTEGER DEFAULT 0,
    is_cover BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 商品评价表
CREATE TABLE product_reviews (
    review_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    order_id UUID NOT NULL,
    rating SMALLINT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(200),
    content TEXT,
    images TEXT[], -- 存储图片URL数组
    is_verified BOOLEAN DEFAULT FALSE,
    status SMALLINT DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_created_at ON products(created_at);
CREATE INDEX idx_products_name_gin ON products USING gin(name gin_trgm_ops);
CREATE INDEX idx_product_reviews_product_id ON product_reviews(product_id);
CREATE INDEX idx_product_reviews_rating ON product_reviews(rating);

-- 创建更新时间触发器
CREATE TRIGGER update_products_updated_at 
    BEFORE UPDATE ON products 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_product_reviews_updated_at 
    BEFORE UPDATE ON product_reviews 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### 3. 订单数据库初始化 (zhi_xuan_order)
```sql
-- 创建数据库
CREATE DATABASE zhi_xuan_order WITH 
    OWNER = order_owner
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

\c zhi_xuan_order;

-- 创建扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 订单状态枚举
CREATE TYPE order_status AS ENUM (
    'pending',      -- 待确认
    'confirmed',    -- 已确认
    'paid',         -- 已支付
    'shipped',      -- 已发货
    'delivered',    -- 已签收
    'cancelled',    -- 已取消
    'refunded'      -- 已退款
);

-- 订单表
CREATE TABLE orders (
    order_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_no VARCHAR(50) UNIQUE NOT NULL,  -- 订单号
    user_id UUID NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    discount_amount DECIMAL(12,2) DEFAULT 0,
    final_amount DECIMAL(12,2) NOT NULL,
    status order_status DEFAULT 'pending',
    payment_method VARCHAR(20),  -- 支付方式
    payment_status VARCHAR(20) DEFAULT 'pending',  -- 支付状态
    shipping_address JSONB,      -- 收货地址JSON
    remark TEXT,                 -- 订单备注
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    paid_at TIMESTAMP WITH TIME ZONE,
    shipped_at TIMESTAMP WITH TIME ZONE,
    delivered_at TIMESTAMP WITH TIME ZONE
);

-- 订单项表
CREATE TABLE order_items (
    order_item_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id UUID NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    product_image VARCHAR(255),
    price DECIMAL(10,2) NOT NULL,
    quantity INTEGER NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 订单支付表
CREATE TABLE order_payments (
    payment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    payment_no VARCHAR(50) NOT NULL,  -- 支付流水号
    payment_method VARCHAR(20) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',  -- pending, success, failed, refunded
    transaction_id VARCHAR(100),  -- 第三方交易号
    gateway_response JSONB,       -- 支付网关响应
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 订单状态历史表
CREATE TABLE order_status_history (
    history_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    old_status order_status,
    new_status order_status NOT NULL,
    remark TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_orders_order_no ON orders(order_no);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_payments_order_id ON order_payments(order_id);
CREATE INDEX idx_order_status_history_order_id ON order_status_history(order_id);

-- 创建订单号生成函数
CREATE OR REPLACE FUNCTION generate_order_no()
RETURNS VARCHAR(50) AS $$
DECLARE
    order_no VARCHAR(50);
BEGIN
    order_no := 'ZXE' || TO_CHAR(NOW(), 'YYYYMMDD') || 
                LPAD(FLOOR(RANDOM() * 1000000)::TEXT, 6, '0');
    RETURN order_no;
END;
$$ LANGUAGE plpgsql;

-- 创建触发器
CREATE TRIGGER update_orders_updated_at 
    BEFORE UPDATE ON orders 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 订单创建触发器，自动生成订单号
CREATE OR REPLACE FUNCTION set_order_no()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.order_no IS NULL THEN
        NEW.order_no := generate_order_no();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_order_no_trigger
    BEFORE INSERT ON orders
    FOR EACH ROW EXECUTE FUNCTION set_order_no();
```

## 读写分离配置

### 1. 应用层读写分离实现
```typescript
// database.service.ts
import { Injectable } from '@nestjs/common';
import { Pool } from 'pg';

@Injectable()
export class DatabaseService {
  private readonly writePool: Pool;  // 主库连接池（写）
  private readonly readPools: Pool[]; // 从库连接池（读）

  constructor() {
    // 主库连接池
    this.writePool = new Pool({
      user: process.env.DB_WRITE_USER || 'user',
      host: process.env.DB_WRITE_HOST || 'master-db',
      database: process.env.DB_NAME || 'zhi_xuan_user',
      password: process.env.DB_WRITE_PASSWORD || 'password',
      port: parseInt(process.env.DB_WRITE_PORT) || 5432,
      max: 20,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });

    // 从库连接池数组
    this.readPools = [
      new Pool({
        user: process.env.DB_READ_USER || 'user',
        host: process.env.DB_READ_HOST_1 || 'slave-1',
        database: process.env.DB_NAME || 'zhi_xuan_user',
        password: process.env.DB_READ_PASSWORD || 'password',
        port: parseInt(process.env.DB_READ_PORT_1) || 5432,
        max: 15,
        idleTimeoutMillis: 30000,
        connectionTimeoutMillis: 2000,
      }),
      new Pool({
        user: process.env.DB_READ_USER || 'user',
        host: process.env.DB_READ_HOST_2 || 'slave-2',
        database: process.env.DB_NAME || 'zhi_xuan_user',
        password: process.env.DB_READ_PASSWORD || 'password',
        port: parseInt(process.env.DB_READ_PORT_2) || 5432,
        max: 15,
        idleTimeoutMillis: 30000,
        connectionTimeoutMillis: 2000,
      })
    ];
  }

  async executeWriteQuery(query: string, params?: any[]) {
    const client = await this.writePool.connect();
    try {
      const result = await client.query(query, params);
      return result;
    } finally {
      client.release();
    }
  }

  async executeReadQuery(query: string, params?: any[]) {
    // 随机选择一个从库连接池
    const randomPool = this.readPools[Math.floor(Math.random() * this.readPools.length)];
    const client = await randomPool.connect();
    try {
      const result = await client.query(query, params);
      return result;
    } finally {
      client.release();
    }
  }

  async executeTransaction(queries: Array<{ query: string; params?: any[] }>) {
    const client = await this.writePool.connect();
    try {
      await client.query('BEGIN');
      
      const results = [];
      for (const { query, params } of queries) {
        const result = await client.query(query, params);
        results.push(result);
      }
      
      await client.query('COMMIT');
      return results;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }
}
```

### 2. 连接池优化配置
```typescript
// config/database.config.ts
import { Pool } from 'pg';

export const createOptimizedPool = (config: {
  host: string,
  port: number,
  database: string,
  user: string,
  password: string,
  max?: number,
  idleTimeoutMillis?: number,
  connectionTimeoutMillis?: number,
  maxLifetimeSeconds?: number
}) => {
  const pool = new Pool({
    host: config.host,
    port: config.port,
    database: config.database,
    user: config.user,
    password: config.password,
    max: config.max || 20,
    idleTimeoutMillis: config.idleTimeoutMillis || 30000,
    connectionTimeoutMillis: config.connectionTimeoutMillis || 2000,
    maxLifetimeSeconds: config.maxLifetimeSeconds || 3600, // 连接最大生命周期1小时
    
    // 连接池事件监听
    onConnect: (client) => {
      // 设置会话参数
      return client.query('SET application_name = $1', ['zhi_xuan_app']);
    }
  });

  // 监听连接池事件
  pool.on('connect', () => {
    console.log('New client connected to database');
  });

  pool.on('acquire', (client) => {
    console.log('Client acquired from pool');
  });

  pool.on('remove', (client) => {
    console.log('Client removed from pool');
  });

  return pool;
};
```

## 数据库性能优化

### 1. 索引优化策略
```sql
-- 为高频查询创建复合索引
CREATE INDEX idx_orders_user_status_created 
ON orders(user_id, status, created_at DESC);

CREATE INDEX idx_products_category_status_price 
ON products(category_id, status, price);

CREATE INDEX idx_product_reviews_product_rating 
ON product_reviews(product_id, rating DESC, created_at DESC);

-- 为全文搜索创建GIN索引
CREATE INDEX idx_products_name_gin 
ON products USING gin(to_tsvector('english', name));

CREATE INDEX idx_products_description_gin 
ON products USING gin(to_tsvector('english', description));

-- 为时间范围查询创建BRIN索引（适用于大表）
CREATE INDEX idx_orders_created_at_brin 
ON orders USING brin(created_at) WITH (pages_per_range = 32);
```

### 2. 查询优化示例
```sql
-- 优化前的查询
SELECT * FROM orders WHERE user_id = '123' AND status = 'paid' ORDER BY created_at DESC LIMIT 20;

-- 优化后的查询（使用覆盖索引）
SELECT order_id, order_no, total_amount, status, created_at 
FROM orders 
WHERE user_id = '123' AND status = 'paid' 
ORDER BY created_at DESC 
LIMIT 20;

-- 使用CTE优化复杂查询
WITH recent_orders AS (
    SELECT order_id, user_id, total_amount, created_at
    FROM orders
    WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
),
order_stats AS (
    SELECT 
        user_id,
        COUNT(*) as order_count,
        SUM(total_amount) as total_spent
    FROM recent_orders
    GROUP BY user_id
)
SELECT 
    u.username,
    u.email,
    os.order_count,
    os.total_spent
FROM users u
JOIN order_stats os ON u.user_id = os.user_id
ORDER BY os.total_spent DESC
LIMIT 10;
```

## 主从复制监控

### 1. 复制延迟监控
```sql
-- 检查主从复制延迟
SELECT 
    client_addr,
    client_hostname,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    write_lag,
    flush_lag,
    replay_lag
FROM pg_stat_replication;

-- 检查复制槽状态
SELECT 
    slot_name,
    active,
    restart_lsn,
    confirmed_flush_lsn,
    (pg_current_wal_lsn() - confirmed_flush_lsn) AS replication_lag_bytes
FROM pg_replication_slots;
```

### 2. 数据库性能监控脚本
```bash
#!/bin/bash
# monitor_db.sh - 数据库性能监控脚本

DB_HOST="localhost"
DB_NAME="zhi_xuan_user"
DB_USER="monitor_user"
DB_PASSWORD="monitor_password"

# 检查数据库连接
check_connection() {
    pg_isready -h $DB_HOST -d $DB_NAME -U $DB_USER
    if [ $? -ne 0 ]; then
        echo "Database connection failed"
        # 发送告警
        send_alert "Database connection failed"
        return 1
    fi
    return 0
}

# 检查主从复制状态
check_replication() {
    # 检查延迟
    DELAY=$(psql -h $DB_HOST -d $DB_NAME -U $DB_USER -t -c "
        SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp())) 
        AS replication_delay 
        FROM pg_stat_replication 
        LIMIT 1;" 2>/dev/null)
    
    if [ ! -z "$DELAY" ] && [ $(echo "$DELAY > 30" | bc) -eq 1 ]; then
        send_alert "Replication delay is $DELAY seconds"
    fi
}

# 检查长事务
check_long_transactions() {
    LONG_TXNS=$(psql -h $DB_HOST -d $DB_NAME -U $DB_USER -t -c "
        SELECT COUNT(*) 
        FROM pg_stat_activity 
        WHERE state = 'active' 
        AND now() - pg_stat_activity.xact_start > interval '5 minutes';")
    
    if [ $LONG_TXNS -gt 0 ]; then
        send_alert "Found $LONG_TXNS long running transactions"
    fi
}

# 发送告警
send_alert() {
    echo "$(date): $1" >> /var/log/db_monitor.log
    # 这里可以集成告警系统，如邮件、短信、钉钉等
}

# 主监控循环
while true; do
    check_connection
    check_replication
    check_long_transactions
    
    sleep 30
done
```

## 数据备份策略

### 1. 自动备份脚本
```bash
#!/bin/bash
# backup_db.sh - 数据库自动备份脚本

BACKUP_DIR="/data/backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# 创建备份目录
mkdir -p $BACKUP_DIR/daily
mkdir -p $BACKUP_DIR/weekly

# 定义数据库列表
DATABASES=("zhi_xuan_user" "zhi_xuan_product" "zhi_xuan_order" "zhi_xuan_inventory" "zhi_xuan_marketing")

# 备份每个数据库
for db in "${DATABASES[@]}"; do
    echo "Starting backup for database: $db"
    
    # 使用pg_dump进行备份
    pg_dump -h localhost -U backup_user -d $db -Fc -f "$BACKUP_DIR/daily/${db}_${DATE}.dump"
    
    if [ $? -eq 0 ]; then
        echo "Backup completed for $db"
    else
        echo "Backup failed for $db"
        # 发送告警
    fi
done

# 清理过期备份
find $BACKUP_DIR -name "*.dump" -mtime +$RETENTION_DAYS -delete

# 执行WAL归档清理
psql -h localhost -U backup_user -d postgres -c "SELECT pg_switch_wal();"
find /var/lib/postgresql/archive -name "*.wal" -mtime +7 -delete
```

### 2. 逻辑备份与物理备份结合
```yaml
# backup_config.yml
backup:
  # 增量备份配置
  incremental:
    enabled: true
    interval: "1 hour"
    wal_archive: true
    
  # 全量备份配置
  full:
    enabled: true
    schedule: "0 2 * * *"  # 每天凌晨2点
    retention: 30          # 保留30天
    
  # 差异备份配置
  differential:
    enabled: true
    schedule: "0 3 * * 0"  # 每周日凌晨3点
    
  # 远程备份
  remote:
    enabled: true
    destination: "s3://zhi_xuan_backups"
    encryption: true
    
  # 验证备份
  verify:
    enabled: true
    after_backup: true
    restore_test: true
```

## 高可用性保障

### 1. 主从切换脚本
```bash
#!/bin/bash
# failover.sh - 主从切换脚本

# 检查主库状态
check_master_status() {
    pg_isready -h $MASTER_HOST -d $DB_NAME -U $DB_USER
    return $?
}

# 执行故障切换
perform_failover() {
    echo "Starting failover procedure..."
    
    # 1. 提升从库为新主库
    psql -h $SLAVE_HOST -d postgres -U $DB_USER -c "SELECT pg_promote();"
    
    # 2. 更新应用配置指向新主库
    update_app_config $SLAVE_HOST
    
    # 3. 重新配置其他从库
    reconfigure_replicas $SLAVE_HOST
    
    # 4. 发送通知
    send_notification "Failover completed. New master is $SLAVE_HOST"
}

# 更新应用配置
update_app_config() {
    local new_master=$1
    
    # 更新配置文件
    sed -i "s/$MASTER_HOST/$new_master/g" /app/config/database.json
    
    # 重启应用服务
    systemctl restart app-service
}

# 检测主库故障并执行切换
if ! check_master_status; then
    echo "Master database is down, initiating failover..."
    perform_failover
fi
```

### 2. 健康检查配置
```typescript
// health-check.service.ts
import { Injectable } from '@nestjs/common';
import { Pool } from 'pg';

@Injectable()
export class DatabaseHealthCheckService {
  private readonly pools: Map<string, Pool> = new Map();

  constructor() {
    // 初始化所有数据库连接池
    this.initPools();
  }

  private initPools() {
    const databases = [
      { name: 'user', host: process.env.USER_DB_HOST },
      { name: 'product', host: process.env.PRODUCT_DB_HOST },
      { name: 'order', host: process.env.ORDER_DB_HOST },
      { name: 'inventory', host: process.env.INVENTORY_DB_HOST },
    ];

    databases.forEach(db => {
      this.pools.set(db.name, new Pool({
        host: db.host,
        database: `zhi_xuan_${db.name}`,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        port: parseInt(process.env.DB_PORT) || 5432,
        max: 5,
        idleTimeoutMillis: 10000,
        connectionTimeoutMillis: 2000,
      }));
    });
  }

  async checkAllHealth() {
    const results = {};
    let allHealthy = true;

    for (const [name, pool] of this.pools) {
      try {
        await this.checkPoolHealth(pool);
        results[name] = { status: 'healthy', latency: await this.getLatency(pool) };
      } catch (error) {
        results[name] = { status: 'unhealthy', error: error.message };
        allHealthy = false;
      }
    }

    // 检查主从复制状态
    const replicationStatus = await this.checkReplicationStatus();
    results.replication = replicationStatus;

    return {
      status: allHealthy ? 'healthy' : 'unhealthy',
      databases: results,
      timestamp: new Date().toISOString(),
    };
  }

  private async checkPoolHealth(pool: Pool) {
    const client = await pool.connect();
    try {
      await client.query('SELECT 1');
    } finally {
      client.release();
    }
  }

  private async getLatency(pool: Pool): Promise<number> {
    const start = Date.now();
    const client = await pool.connect();
    try {
      await client.query('SELECT 1');
      return Date.now() - start;
    } finally {
      client.release();
    }
  }

  private async checkReplicationStatus() {
    // 检查主从复制状态的逻辑
    try {
      const masterPool = this.pools.get('user'); // 假设user库为主库
      const result = await masterPool.query(`
        SELECT 
          client_addr,
          state,
          EXTRACT(EPOCH FROM (now() - replay_lag)) as delay_seconds
        FROM pg_stat_replication
      `);
      
      return {
        status: 'healthy',
        slaves: result.rows.map(row => ({
          address: row.client_addr,
          state: row.state,
          delay: row.delay_seconds
        }))
      };
    } catch (error) {
      return { status: 'unhealthy', error: error.message };
    }
  }
}
```

这个数据库架构设计包含了：

1. 详细的分库分表策略
2. PostgreSQL主从复制配置
3. 各数据库的表结构设计
4. 读写分离实现
5. 性能优化策略
6. 监控和备份方案
7. 高可用性保障措施

架构设计确保了数据的高可用性、高性能和可扩展性，满足智选电商平台的业务需求。