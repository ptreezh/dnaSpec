#!/usr/bin/env node

/**
 * 测试 stigmergylite 作为 npm 包的使用
 */

const GitAutoInstaller = require('stigmergylite');

async function testAsNpmPackage() {
  console.log('🧪 测试 stigmergylite 作为 npm 包\n');

  // 创建安装器实例
  const installer = new GitAutoInstaller({
    autoInstall: true,           // 自动安装 Git（如果需要）
    configureGitBash: true,      // 配置 Git Bash 路径
    installOpenCode: true,       // 安装 OpenCode
    installBun: true,            // 安装 Bun
    installOhMyOpenCode: true,   // 安装 Oh My OpenCode
    silent: false                // 显示详细输出
  });

  try {
    // 执行安装
    const result = await installer.install();

    console.log('\n✅ 测试成功！\n');
    console.log('安装结果:');
    console.log('- 成功:', result.success);
    console.log('- 操作系统:', result.os);
    console.log('- Git 已安装:', result.git.installed);
    console.log('- Git 版本:', result.git.version);
    console.log('- Git Bash 路径:', result.gitBashPath);
    console.log('- OpenCode 已安装:', result.opencode);
    console.log('- Bun 已安装:', result.bun);

    console.log('\n✅ stigmergylite 作为 npm 包工作正常！');

    return result;
  } catch (error) {
    console.error('\n❌ 测试失败:', error.message);
    throw error;
  }
}

// 运行测试
testAsNpmPackage()
  .then(() => {
    console.log('\n🎉 所有测试通过！');
  })
  .catch(error => {
    console.error('\n❌ 测试失败:', error);
    process.exit(1);
  });