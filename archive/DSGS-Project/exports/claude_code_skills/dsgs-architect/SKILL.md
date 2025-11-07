---
name: dsgs-architect
description: "DSGS智能架构师主技能，用于复杂项目的分层架构设计、任务分解、智能体化和约束生成。当用户提到复杂项目架构设计、系统架构规划、多层架构分解或智能体系统创建时使用此技能。不要在讨论具体技术实现细节时使用。"
---

# DSGS智能架构师主技能

## 功能概述
dsgs-architect是DSGS智能架构师系统的核心协调技能，负责：
1. 接收用户关于复杂项目的需求
2. 分析需求并路由到相应的子技能
3. 协调各子技能间的工作流
4. 整合各子技能的输出结果
5. 生成最终的架构设计文档

## 使用方法
作为Claude Skills的一部分，该技能会根据描述自动被Claude调用。

## 技能协调
该技能协调以下子技能：
- dsgs-system-architect: 系统架构设计
- dsgs-task-decomposer: 任务分解
- dsgs-agent-creator: 智能体创建
- dsgs-constraint-generator: 约束生成

## 输出格式
技能输出完整的项目架构设计文档，包括：
- 系统架构图
- 任务分解结构
- 智能体规范
- 约束定义