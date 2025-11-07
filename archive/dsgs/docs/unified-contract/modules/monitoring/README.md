# 服务监控模块

## 📋 模块概览

服务监控模块负责DSGS系统的健康检查、性能指标收集、自动恢复和告警通知。确保系统的高可用性和可观测性。

### 🎯 核心功能
- **实时健康检查**：监控所有核心组件的健康状态
- **性能指标收集**：收集系统性能和业务指标
- **自动恢复机制**：故障时自动恢复服务
- **智能告警**：基于规则的告警和通知

### 📊 监控范围
| 组件 | 监控内容 | 告警阈值 |
|------|----------|----------|
| **MCP服务器** | 连接状态、消息处理延迟、错误率 | 延迟>1s，错误率>5% |
| **约束生成器** | 生成时间、成功率、模板匹配 | 生成时间>100ms，成功率<95% |
| **神经场处理** | 冲突检测时间、收敛速度 | 检测时间>500ms，收敛时间>1s |
| **数据库** | 连接池状态、查询性能 | 连接失败率>1%，查询时间>100ms |
| **系统资源** | CPU、内存、磁盘、网络 | CPU>80%，内存>85% |

## 🔗 快速导航

### 📖 核心文档
- [健康检查API](#健康检查-api) - 健康检查接口定义
- [指标收集API](#指标收集-api) - 性能指标接口
- [告警管理API](#告警管理-api) - 告警管理接口
- [数据模型](#数据模型) - 监控相关数据结构

### 🔧 实现指南
- [健康检查实现](#健康检查实现) - 健康检查服务实现
- [指标收集实现](#指标收集实现) - 指标收集器实现
- [自动恢复实现](#自动恢复实现) - 自动恢复机制实现
- [告警系统实现](#告警系统实现) - 告警系统实现

### 📊 配置指南
- [监控配置](#监控配置) - 监控组件配置
- [告警配置](#告警配置) - 告警规则配置
- [存储配置](#存储配置) - 数据存储配置

## 🚀 API接口

### 健康检查 API

#### 获取系统健康状态
```typescript
// GET /api/monitoring/health
interface HealthResponse {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  version: string;
  uptime: number;
  components: ComponentHealth[];
  metrics: SystemMetrics;
  issues: HealthIssue[];
  recommendations: string[];
}
```

**示例请求**：
```bash
curl -X GET "http://localhost:3000/api/monitoring/health" \
  -H "Authorization: Bearer ${TOKEN}"
```

**示例响应**：
```json
{
  "status": "healthy",
  "timestamp": "2025-08-06T10:00:00Z",
  "version": "2.0.0",
  "uptime": 86400,
  "components": [
    {
      "name": "mcpServer",
      "status": "healthy",
      "details": "Running normally",
      "lastCheck": "2025-08-06T10:00:00Z",
      "metrics": {
        "activeConnections": 15,
        "messageProcessingTime": 45
      }
    }
  ],
  "metrics": {
    "cpu": 25.5,
    "memory": 67.2,
    "disk": 45.8
  },
  "issues": [],
  "recommendations": []
}
```

#### 获取组件健康状态
```typescript
// GET /api/monitoring/health/components/{componentName}
interface ComponentHealthResponse {
  name: string;
  status: 'healthy' | 'degraded' | 'unhealthy';
  details: string;
  lastCheck: string;
  metrics: ComponentMetrics;
  dependencies: string[];
  history: HealthHistory[];
}
```

### 指标收集 API

#### 获取系统指标
```typescript
// GET /api/monitoring/metrics
interface MetricsResponse {
  system: SystemMetrics;
  components: ComponentMetrics[];
  business: BusinessMetrics[];
  custom: CustomMetric[];
  timestamp: string;
}
```

#### 获取特定指标
```typescript
// GET /api/monitoring/metrics/{metricName}
interface MetricResponse {
  name: string;
  value: number;
  labels: Record<string, string>;
  timestamp: string;
  history: MetricHistory[];
}
```

### 告警管理 API

#### 获取活跃告警
```typescript
// GET /api/monitoring/alerts
interface AlertsResponse {
  alerts: Alert[];
  totalCount: number;
  filteredCount: number;
  page: number;
  limit: number;
}
```

#### 解决告警
```typescript
// POST /api/monitoring/alerts/{alertId}/resolve
interface ResolveAlertResponse {
  success: boolean;
  message: string;
  resolvedAt: string;
  resolvedBy: string;
}
```

## 📊 数据模型

### 核心数据模型

#### 健康状态 (HealthStatus)
```typescript
interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  version: string;
  uptime: number;
  components: ComponentHealth[];
  metrics: SystemMetrics;
  issues: HealthIssue[];
  recommendations: string[];
}

interface ComponentHealth {
  name: string;
  status: 'healthy' | 'degraded' | 'unhealthy';
  details: string;
  lastCheck: string;
  metrics?: ComponentMetrics;
  dependencies?: string[];
}

interface HealthIssue {
  id: string;
  type: 'performance' | 'connection' | 'resource' | 'business';
  severity: 'low' | 'medium' | 'high' | 'critical';
  message: string;
  component?: string;
  timestamp: string;
  resolved: boolean;
  resolvedAt?: string;
  resolvedBy?: string;
}
```

#### 系统指标 (SystemMetrics)
```typescript
interface SystemMetrics {
  cpu: {
    usage: number;
    cores: number;
    loadAverage: number[];
  };
  memory: {
    total: number;
    used: number;
    free: number;
    usage: number;
  };
  disk: {
    total: number;
    used: number;
    free: number;
    usage: number;
  };
  network: {
    bytesIn: number;
    bytesOut: number;
    packetsIn: number;
    packetsOut: number;
  };
}

interface ComponentMetrics {
  requestCount: number;
  errorCount: number;
  averageResponseTime: number;
  lastRequestTime: string;
  customMetrics: Record<string, number>;
}
```

#### 告警 (Alert)
```typescript
interface Alert {
  id: string;
  name: string;
  description: string;
  type: 'performance' | 'connection' | 'resource' | 'business';
  severity: 'low' | 'medium' | 'high' | 'critical';
  status: 'active' | 'resolved' | 'suppressed';
  component?: string;
  metric?: string;
  threshold: number;
  currentValue: number;
  triggeredAt: string;
  resolvedAt?: string;
  resolvedBy?: string;
  notifications: Notification[];
}

interface Notification {
  id: string;
  channel: 'email' | 'slack' | 'webhook';
  recipient: string;
  sentAt: string;
  status: 'sent' | 'failed' | 'delivered';
}
```

## 🔧 实现细节

### 健康检查实现

#### 健康检查服务
```typescript
// src/core/monitoring/HealthCheckService.ts
export class HealthCheckService {
  private components: Map<string, HealthChecker> = new Map();
  private metrics: MetricsCollector;
  private recoveryManager: RecoveryManager;
  
  constructor() {
    this.initializeComponents();
    this.startHealthChecks();
  }
  
  private initializeComponents() {
    // 注册所有需要监控的组件
    this.components.set('mcpServer', new McpServerHealthChecker());
    this.components.set('constraintGenerator', new ConstraintGeneratorHealthChecker());
    this.components.set('neuralField', new NeuralFieldHealthChecker());
    this.components.set('database', new DatabaseHealthChecker());
  }
  
  async getSystemHealth(): Promise<HealthStatus> {
    const componentHealths = await Promise.all(
      Array.from(this.components.values()).map(checker => checker.check())
    );
    
    const overallStatus = this.calculateOverallStatus(componentHealths);
    const metrics = await this.metrics.collectSystemMetrics();
    const issues = this.identifyIssues(componentHealths);
    const recommendations = this.generateRecommendations(issues);
    
    return {
      status: overallStatus,
      timestamp: new Date().toISOString(),
      version: process.env.VERSION || '2.0.0',
      uptime: process.uptime(),
      components: componentHealths,
      metrics,
      issues,
      recommendations
    };
  }
  
  private calculateOverallStatus(components: ComponentHealth[]): HealthStatus['status'] {
    const hasUnhealthy = components.some(c => c.status === 'unhealthy');
    const hasDegraded = components.some(c => c.status === 'degraded');
    
    if (hasUnhealthy) return 'unhealthy';
    if (hasDegraded) return 'degraded';
    return 'healthy';
  }
}
```

#### 组件健康检查器
```typescript
// src/core/monitoring/checkers/McpServerHealthChecker.ts
export class McpServerHealthChecker implements HealthChecker {
  private mcpServer: McpServer;
  
  constructor(mcpServer: McpServer) {
    this.mcpServer = mcpServer;
  }
  
  async check(): Promise<ComponentHealth> {
    try {
      const startTime = Date.now();
      
      // 检查连接状态
      const isConnected = await this.mcpServer.isConnected();
      if (!isConnected) {
        return {
          name: 'mcpServer',
          status: 'unhealthy',
          details: 'MCP server is not connected',
          lastCheck: new Date().toISOString()
        };
      }
      
      // 检查消息处理延迟
      const processingTime = await this.mcpServer.getProcessingTime();
      const activeConnections = await this.mcpServer.getActiveConnections();
      
      // 确定健康状态
      let status: ComponentHealth['status'] = 'healthy';
      let details = 'Running normally';
      
      if (processingTime > 1000) {
        status = 'degraded';
        details = `High processing time: ${processingTime}ms`;
      }
      
      if (processingTime > 5000) {
        status = 'unhealthy';
        details = `Critical processing time: ${processingTime}ms`;
      }
      
      return {
        name: 'mcpServer',
        status,
        details,
        lastCheck: new Date().toISOString(),
        metrics: {
          activeConnections,
          messageProcessingTime: processingTime,
          checkDuration: Date.now() - startTime
        }
      };
      
    } catch (error) {
      return {
        name: 'mcpServer',
        status: 'unhealthy',
        details: `Health check failed: ${error.message}`,
        lastCheck: new Date().toISOString()
      };
    }
  }
}
```

### 指标收集实现

#### 指标收集器
```typescript
// src/core/monitoring/MetricsCollector.ts
export class MetricsCollector {
  private prometheusClient: PrometheusClient;
  private metrics: Map<string, Metric> = new Map();
  
  constructor() {
    this.prometheusClient = new PrometheusClient();
    this.initializeMetrics();
  }
  
  private initializeMetrics() {
    // 系统指标
    this.createGauge('system_cpu_usage_percent', 'System CPU usage percentage');
    this.createGauge('system_memory_usage_bytes', 'System memory usage in bytes');
    this.createGauge('system_disk_usage_bytes', 'System disk usage in bytes');
    
    // MCP服务器指标
    this.createCounter('mcp_requests_total', 'Total MCP requests', ['method', 'status']);
    this.createHistogram('mcp_request_duration_seconds', 'MCP request duration', ['method']);
    this.createGauge('mcp_active_connections', 'Active MCP connections');
    
    // 约束生成器指标
    this.createHistogram('constraint_generation_duration', 'Constraint generation duration');
    this.createCounter('constraint_template_matches_total', 'Total template matches', ['template_id']);
    this.createCounter('constraint_validation_errors_total', 'Total validation errors', ['error_type']);
    
    // 神经场指标
    this.createHistogram('neural_field_processing_time', 'Neural field processing time');
    this.createCounter('constraint_conflicts_detected_total', 'Total constraint conflicts detected');
    this.createHistogram('attractor_convergence_time', 'Attractor convergence time');
  }
  
  recordMcpRequest(method: string, duration: number, status: string) {
    this.metrics.get('mcp_requests_total')?.inc({ method, status });
    this.metrics.get('mcp_request_duration_seconds')?.observe({ method }, duration);
  }
  
  recordConstraintGeneration(duration: number, templateId?: string) {
    this.metrics.get('constraint_generation_duration')?.observe(duration);
    if (templateId) {
      this.metrics.get('constraint_template_matches_total')?.inc({ template_id: templateId });
    }
  }
  
  async collectSystemMetrics(): Promise<SystemMetrics> {
    const cpuUsage = await this.getCpuUsage();
    const memoryUsage = await this.getMemoryUsage();
    const diskUsage = await this.getDiskUsage();
    const networkUsage = await this.getNetworkUsage();
    
    return {
      cpu: cpuUsage,
      memory: memoryUsage,
      disk: diskUsage,
      network: networkUsage
    };
  }
}
```

### 自动恢复实现

#### 恢复管理器
```typescript
// src/core/monitoring/RecoveryManager.ts
export class RecoveryManager {
  private recoveryStrategies: Map<string, RecoveryStrategy> = new Map();
  private healthCheckService: HealthCheckService;
  private alertManager: AlertManager;
  
  constructor() {
    this.initializeRecoveryStrategies();
    this.startMonitoring();
  }
  
  private initializeRecoveryStrategies() {
    this.recoveryStrategies.set('mcpServer', new McpServerRecoveryStrategy());
    this.recoveryStrategies.set('constraintGenerator', new ConstraintGeneratorRecoveryStrategy());
    this.recoveryStrategies.set('neuralField', new NeuralFieldRecoveryStrategy());
  }
  
  private startMonitoring() {
    setInterval(async () => {
      const health = await this.healthCheckService.getSystemHealth();
      
      for (const component of health.components) {
        if (component.status !== 'healthy') {
          await this.attemptRecovery(component.name, component.status);
        }
      }
    }, 30000); // 每30秒检查一次
  }
  
  private async attemptRecovery(componentName: string, status: ComponentHealth['status']) {
    const strategy = this.recoveryStrategies.get(componentName);
    if (!strategy) return;
    
    try {
      console.log(`Attempting recovery for ${componentName} (${status})`);
      await strategy.recover(status);
      
      // 验证恢复是否成功
      await this.verifyRecovery(componentName);
      
    } catch (error) {
      console.error(`Recovery failed for ${componentName}:`, error);
      // 触发告警
      await this.alertManager.createAlert({
        name: `Recovery Failed: ${componentName}`,
        description: `Automatic recovery failed for ${componentName}: ${error.message}`,
        type: 'system',
        severity: 'high',
        component: componentName
      });
    }
  }
  
  private async verifyRecovery(componentName: string) {
    const health = await this.healthCheckService.getComponentHealth(componentName);
    
    if (health.status === 'healthy') {
      console.log(`Recovery successful for ${componentName}`);
    } else {
      throw new Error(`Recovery verification failed for ${componentName}`);
    }
  }
}
```

#### 恢复策略
```typescript
// src/core/monitoring/strategies/McpServerRecoveryStrategy.ts
export class McpServerRecoveryStrategy implements RecoveryStrategy {
  private mcpServer: McpServer;
  
  constructor(mcpServer: McpServer) {
    this.mcpServer = mcpServer;
  }
  
  async recover(status: ComponentHealth['status']): Promise<void> {
    switch (status) {
      case 'degraded':
        await this.restartGracefully();
        break;
      case 'unhealthy':
        await this.forceRestart();
        break;
    }
  }
  
  private async restartGracefully() {
    console.log('Gracefully restarting MCP server...');
    
    // 停止接受新连接
    await this.mcpServer.stopAcceptingConnections();
    
    // 等待现有请求完成
    await this.waitForRequestsToComplete(30000); // 30秒超时
    
    // 重启服务
    await this.mcpServer.restart();
    
    console.log('MCP server restarted gracefully');
  }
  
  private async forceRestart() {
    console.log('Force restarting MCP server...');
    
    // 立即停止服务
    await this.mcpServer.forceStop();
    
    // 等待进程完全停止
    await this.sleep(5000);
    
    // 重启服务
    await this.mcpServer.restart();
    
    console.log('MCP server force restarted');
  }
  
  private async waitForRequestsToComplete(timeout: number): Promise<void> {
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeout) {
      const activeRequests = await this.mcpServer.getActiveRequests();
      if (activeRequests === 0) {
        return;
      }
      await this.sleep(1000);
    }
    
    throw new Error('Timeout waiting for requests to complete');
  }
  
  private async sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

## ⚙️ 配置

### 监控配置
```typescript
// src/config/monitoring.config.ts
export interface MonitoringConfig {
  enabled: boolean;
  healthCheck: {
    interval: number;        // 健康检查间隔（毫秒）
    timeout: number;         // 健康检查超时（毫秒）
    retries: number;        // 重试次数
  };
  metrics: {
    enabled: boolean;
    collectionInterval: number;  // 指标收集间隔（毫秒）
    retentionDays: number;       // 指标保留天数
    prometheus: {
      enabled: boolean;
      port: number;
      path: string;
    };
  };
  alerts: {
    enabled: boolean;
    channels: {
      email: {
        enabled: boolean;
        smtp: {
          host: string;
          port: number;
          secure: boolean;
          auth: {
            user: string;
            pass: string;
          };
        };
      };
      slack: {
        enabled: boolean;
        webhook: string;
        channel: string;
      };
    };
  };
  recovery: {
    enabled: boolean;
    maxAttempts: number;     // 最大恢复尝试次数
    backoffMultiplier: number; // 退避倍数
    maxBackoffTime: number;   // 最大退避时间
  };
}

const defaultConfig: MonitoringConfig = {
  enabled: true,
  healthCheck: {
    interval: 30000,    // 30秒
    timeout: 5000,      // 5秒
    retries: 3
  },
  metrics: {
    enabled: true,
    collectionInterval: 10000,  // 10秒
    retentionDays: 30,
    prometheus: {
      enabled: true,
      port: 9090,
      path: '/metrics'
    }
  },
  alerts: {
    enabled: true,
    channels: {
      email: {
        enabled: false,
        smtp: {
          host: 'smtp.gmail.com',
          port: 587,
          secure: false,
          auth: {
            user: process.env.EMAIL_USER,
            pass: process.env.EMAIL_PASS
          }
        }
      },
      slack: {
        enabled: false,
        webhook: process.env.SLACK_WEBHOOK,
        channel: '#alerts'
      }
    }
  },
  recovery: {
    enabled: true,
    maxAttempts: 3,
    backoffMultiplier: 2,
    maxBackoffTime: 300000  // 5分钟
  }
};
```

### 告警规则配置
```typescript
// src/config/alert-rules.config.ts
export interface AlertRule {
  id: string;
  name: string;
  description: string;
  condition: AlertCondition;
  severity: 'low' | 'medium' | 'high' | 'critical';
  duration: number;        // 持续时间（毫秒）
  enabled: boolean;
  notifications: {
    channels: ('email' | 'slack' | 'webhook')[];
    recipients: string[];
  };
}

export interface AlertCondition {
  metric: string;
  operator: 'gt' | 'lt' | 'eq' | 'ne';
  threshold: number;
  labels?: Record<string, string>;
}

const alertRules: AlertRule[] = [
  {
    id: 'cpu-usage-high',
    name: 'CPU Usage High',
    description: 'CPU usage is above 80%',
    condition: {
      metric: 'system_cpu_usage_percent',
      operator: 'gt',
      threshold: 80
    },
    severity: 'high',
    duration: 300000,  // 5分钟
    enabled: true,
    notifications: {
      channels: ['email', 'slack'],
      recipients: ['admin@example.com']
    }
  },
  {
    id: 'memory-usage-high',
    name: 'Memory Usage High',
    description: 'Memory usage is above 85%',
    condition: {
      metric: 'system_memory_usage_percent',
      operator: 'gt',
      threshold: 85
    },
    severity: 'high',
    duration: 300000,  // 5分钟
    enabled: true,
    notifications: {
      channels: ['email', 'slack'],
      recipients: ['admin@example.com']
    }
  },
  {
    id: 'mcp-response-time-high',
    name: 'MCP Response Time High',
    description: 'MCP server response time is above 1 second',
    condition: {
      metric: 'mcp_request_duration_seconds',
      operator: 'gt',
      threshold: 1,
      labels: { method: 'checkConstraints' }
    },
    severity: 'medium',
    duration: 180000,  // 3分钟
    enabled: true,
    notifications: {
      channels: ['slack'],
      recipients: ['#dev-alerts']
    }
  }
];
```

## 📊 监控仪表板

### Grafana仪表板配置

```json
{
  "dashboard": {
    "title": "DSGS System Monitoring",
    "panels": [
      {
        "title": "System Health",
        "type": "stat",
        "targets": [
          {
            "expr": "dsgs_system_health_status",
            "legendFormat": "{{status}}"
          }
        ]
      },
      {
        "title": "CPU Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "system_cpu_usage_percent",
            "legendFormat": "CPU Usage"
          }
        ]
      },
      {
        "title": "Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "system_memory_usage_percent",
            "legendFormat": "Memory Usage"
          }
        ]
      },
      {
        "title": "MCP Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(mcp_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ]
      },
      {
        "title": "Constraint Generation Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, constraint_generation_duration_bucket)",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, constraint_generation_duration_bucket)",
            "legendFormat": "50th percentile"
          }
        ]
      }
    ]
  }
}
```

## 🧪 测试

### 单元测试
```typescript
// src/test/monitoring/HealthCheckService.spec.ts
describe('HealthCheckService', () => {
  let healthCheckService: HealthCheckService;
  let mockMetricsCollector: MetricsCollector;
  
  beforeEach(() => {
    mockMetricsCollector = createMock<MetricsCollector>();
    healthCheckService = new HealthCheckService();
  });
  
  it('should return system health status', async () => {
    const health = await healthCheckService.getSystemHealth();
    
    expect(health.status).toBeOneOf(['healthy', 'degraded', 'unhealthy']);
    expect(health.timestamp).toBeDefined();
    expect(health.components).toHaveLength(4);
  });
  
  it('should detect unhealthy component', async () => {
    // 模拟不健康的组件
    jest.spyOn(healthCheckService['components'].get('mcpServer')!, 'check')
      .mockResolvedValue({
        name: 'mcpServer',
        status: 'unhealthy',
        details: 'Connection failed',
        lastCheck: new Date().toISOString()
      });
    
    const health = await healthCheckService.getSystemHealth();
    
    expect(health.status).toBe('unhealthy');
    expect(health.components.find(c => c.name === 'mcpServer')?.status)
      .toBe('unhealthy');
  });
});
```

### 集成测试
```typescript
// src/test/monitoring/MonitoringIntegration.spec.ts
describe('Monitoring Integration', () => {
  let app: Application;
  let metricsCollector: MetricsCollector;
  
  beforeAll(async () => {
    app = await createTestApp();
    metricsCollector = app.get(MetricsCollector);
  });
  
  it('should collect MCP request metrics', async () => {
    // 模拟MCP请求
    await request(app.getHttpServer())
      .post('/mcp')
      .send({
        method: 'checkConstraints',
        params: { tccPath: 'test.tcc', specPath: 'test.json' }
      });
    
    // 验证指标被收集
    const metrics = await metricsCollector.getMetrics();
    expect(metrics.get('mcp_requests_total')).toBeDefined();
  });
  
  it('should trigger alert on unhealthy component', async () => {
    // 模拟不健康状态
    await metricsCollector.recordComponentHealth('mcpServer', 'unhealthy');
    
    // 验证告警被触发
    const alerts = await app.get(AlertService).getActiveAlerts();
    expect(alerts.some(a => a.component === 'mcpServer')).toBe(true);
  });
});
```

## 🔗 相关文档

### 核心文档
- [系统架构总览](../architecture/overview.md) - 系统整体架构
- [API契约总览](../api/contract-overview.md) - API接口契约
- [数据模型字典](../data-models/dictionary.md) - 数据结构定义

### 相关模块
- [契约管理模块](../contract/README.md) - 契约生成和验证
- [约束生成模块](../constraint/README.md) - 动态约束生成
- [MCP协议模块](../mcp/README.md) - MCP协议实现

### 规范文档
- [命名规范](../standards/naming-conventions.md) - 统一命名规范
- [错误处理](../standards/error-handling.md) - 错误处理机制
- [版本管理](../standards/versioning.md) - 版本兼容性管理

---

**模块维护**：DSGS监控团队  
**最后更新**：2025-08-06  
**版本**：2.0