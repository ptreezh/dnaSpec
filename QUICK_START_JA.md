# DNASPEC コンテキスト工学スキル - クイックスタートガイド (Japanese)

## プロジェクト概要

DNASPEC (Dynamic Specification Growth System) コンテキスト工学スキルは、AI CLIプラットフォーム向けに特別設計されたプロフェッショナルなAI支援開発ツールキットで、コンテキスト分析、最適化、認知テンプレート機能とAIセーフティワークフローを提供します。

## 主な改善点

### 1. 統一スキルアーキテクチャ
- **統合実装**: 標準モードと強化モードのスキルが単一実装にマージ
- **モード切替**: `mode` パラメータを使用して機能レベルを制御 ('standard' または 'enhanced')
- **単一インターフェース**: 重複機能を避ける簡素化されたインターフェース

### 2. 平坦ディレクトリ構造
- **1スキル1ディレクトリ**: 各スキルが独自ディレクトリに、不要なネストなし
- **簡素化された組織**: 直感的なスキル配置、容易なメンテナンス
- **混乱の削減**: 明確なスキル境界、機能重複なし

### 3. AIセーフティーワークフロー
- **一時ワークスペース**: AI生成コンテンツはまず一時領域に保存
- **自動管理**: ファイル数が20を超えると自動アラート
- **確認メカニズム**: メインプロジェクトへの含める前にコンテンツ確認が必要
- **自動クリーンアップ**: タスク完了後の一時ワークスペースの自動クリア

## インストール

```bash
# リポジトリをクローン
git clone https://github.com/ptreezh/dnaSpec.git
cd dnaspec-context-engineering

# インストール
pip install -e .
```

## 使用方法

### CLIコマンド
```
/speckit.dnaspec.context-analysis "この要件ドキュメントの品質を分析" mode=enhanced
/speckit.dnaspec.cognitive-template "パフォーマンスをどう改善するか" template=verification
/speckit.dnaspec.context-optimization "この要件を最適化" optimization_goals=clarity,relevance
/speckit.dnaspec.architect "ECシステムアーキテクチャを設計"
/speckit.dnaspec.git-skill operation=status
/speckit.dnaspec.temp-workspace operation=create-workspace
```

### Python API
```python
from clean_skills.context_analysis import execute as context_analysis_execute

# スタンダードモード
result = context_analysis_execute({
    'context': 'ユーザーログイン機能を設計',
    'mode': 'standard'
})

# エンハンスドモード
result = context_analysis_execute({
    'context': 'セキュアなユーザー認証機能を設計',
    'mode': 'enhanced'
})
```

## AIセーフティーベストプラクティス

1. **AI生成前** : 常に一時作業スペースを最初に作成
2. **コンテンツ検証** : 確認メカニズムを使用してAI生成コンテンツを検証
3. **定期的なクリーンアップ**: 一時ファイル数を監視
4. **ワークスペースクリア**: タスク完了後に一時領域をクリア

---
*著者: pTree 張博士*  
*機関: AIパーソナ・ラボ2025*  
*連絡先: 3061176@qq.com*  
*ウェブサイト: https://AgentPsy.com*