#!/usr/bin/env python3
"""
DNASPEC CLI Command Manager

Provides atomic deployment and removal of CLI commands across multiple AI platforms.
Implements transaction-like operations with automatic rollback on failure.

Usage:
    python tools/cli_command_manager.py deploy --platforms iflow,claude,copilot
    python tools/cli_command_manager.py remove --platforms iflow,claude,copilot
    python tools/cli_command_manager.py rollback <transaction-id>
    python tools/cli_command_manager.py status
"""

import os
import sys
import json
import shutil
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class Transaction:
    """Represents a deployment/removal transaction"""
    id: str
    operation: str  # 'deploy' or 'remove'
    platforms: List[str]
    timestamp: str
    status: str  # 'pending', 'completed', 'failed', 'rolled_back'
    backup_path: Optional[str] = None
    error: Optional[str] = None


class CLICommandManager:
    """Manages CLI command deployment with atomic operations"""

    # Supported AI CLI platforms
    PLATFORMS = ['iflow', 'claude', 'copilot', 'gemini', 'qwen', 'qodercli', 'codebuddy']

    # Command definitions
    COMMANDS = [
        'dnaspec-agent-creator',
        'dnaspec-architect',
        'dnaspec-cache-manager',
        'dnaspec-constraint-generator',
        'dnaspec-dapi-checker',
        'dnaspec-git-operations',
        'dnaspec-modulizer',
        'dnaspec-task-decomposer'
    ]

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.transactions_dir = self.project_root / '.dnaspec' / 'transactions'
        self.backup_dir = self.project_root / '.dnaspec' / 'backups'
        self.transactions_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def _generate_transaction_id(self) -> str:
        """Generate unique transaction ID"""
        timestamp = datetime.now().isoformat()
        data = f"{timestamp}-{os.getpid()}"
        return hashlib.md5(data.encode()).hexdigest()[:12]

    def _get_platform_commands_dir(self, platform: str) -> Path:
        """Get commands directory for a platform"""
        return self.project_root / f'.{platform}' / 'commands'

    def _backup_commands(self, platforms: List[str]) -> Path:
        """Create backup of existing commands before modification"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}"

        for platform in platforms:
            commands_dir = self._get_platform_commands_dir(platform)
            if commands_dir.exists():
                backup_platform_dir = backup_path / platform
                shutil.copytree(commands_dir, backup_platform_dir)

        return backup_path

    def _restore_backup(self, backup_path: Path, platforms: List[str]) -> bool:
        """Restore commands from backup"""
        try:
            for platform in platforms:
                commands_dir = self._get_platform_commands_dir(platform)
                backup_platform_dir = backup_path / platform

                # Remove existing commands
                if commands_dir.exists():
                    shutil.rmtree(commands_dir)

                # Restore from backup if it exists
                if backup_platform_dir.exists():
                    shutil.copytree(backup_platform_dir, commands_dir)

            return True
        except Exception as e:
            print(f"Error restoring backup: {e}")
            return False

    def _validate_commands(self, platforms: List[str]) -> bool:
        """Validate that commands are properly deployed"""
        try:
            for platform in platforms:
                commands_dir = self._get_platform_commands_dir(platform)

                if not commands_dir.exists():
                    print(f"Validation failed: {platform} commands directory does not exist")
                    return False

                # Check for expected command files
                for command in self.COMMANDS:
                    command_file = commands_dir / f"{command}.md"
                    if not command_file.exists():
                        print(f"Validation failed: {platform} command {command} not found")
                        return False

            return True
        except Exception as e:
            print(f"Validation error: {e}")
            return False

    def _save_transaction(self, transaction: Transaction):
        """Save transaction state to disk"""
        transaction_file = self.transactions_dir / f"{transaction.id}.json"
        with open(transaction_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(transaction), f, indent=2, ensure_ascii=False)

    def _load_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Load transaction state from disk"""
        transaction_file = self.transactions_dir / f"{transaction_id}.json"
        if not transaction_file.exists():
            return None

        with open(transaction_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return Transaction(**data)

    def deploy(self, platforms: List[str], source_dir: Optional[Path] = None) -> bool:
        """
        Atomically deploy commands to specified platforms.

        Args:
            platforms: List of platform names
            source_dir: Source directory containing command templates

        Returns:
            True if successful, False otherwise
        """
        print(f"🚀 Starting atomic deployment to platforms: {', '.join(platforms)}")

        # Validate platforms
        invalid_platforms = [p for p in platforms if p not in self.PLATFORMS]
        if invalid_platforms:
            print(f"❌ Invalid platforms: {', '.join(invalid_platforms)}")
            print(f"Valid platforms: {', '.join(self.PLATFORMS)}")
            return False

        # Create transaction
        transaction = Transaction(
            id=self._generate_transaction_id(),
            operation='deploy',
            platforms=platforms,
            timestamp=datetime.now().isoformat(),
            status='pending'
        )

        try:
            # Step 1: Backup existing state
            print("📦 Step 1: Creating backup...")
            backup_path = self._backup_commands(platforms)
            transaction.backup_path = str(backup_path)
            self._save_transaction(transaction)
            print(f"✅ Backup created: {backup_path}")

            # Step 2: Deploy commands
            print("📝 Step 2: Deploying commands...")
            if source_dir is None:
                # Use default source (archive_uncertain or spec-kit)
                source_dir = self.project_root / 'archive_uncertain'

            for platform in platforms:
                commands_dir = self._get_platform_commands_dir(platform)
                commands_dir.mkdir(parents=True, exist_ok=True)

                source_platform_dir = source_dir / f'.{platform}' / 'commands'

                if source_platform_dir.exists():
                    # Copy command files
                    for command in self.COMMANDS:
                        source_file = source_platform_dir / f"{command}.md"
                        dest_file = commands_dir / f"{command}.md"

                        if source_file.exists():
                            shutil.copy2(source_file, dest_file)
                            print(f"  ✓ {platform}/{command}.md")
                        else:
                            print(f"  ⚠ {platform}/{command}.md not found in source")

            # Step 3: Validate deployment
            print("🔍 Step 3: Validating deployment...")
            if not self._validate_commands(platforms):
                raise Exception("Deployment validation failed")

            # Step 4: Mark transaction as completed
            transaction.status = 'completed'
            self._save_transaction(transaction)

            print(f"✅ Deployment completed successfully!")
            print(f"Transaction ID: {transaction.id}")
            return True

        except Exception as e:
            # Rollback on failure
            print(f"\n❌ Deployment failed: {e}")
            print("🔄 Rolling back...")

            if transaction.backup_path:
                if self._restore_backup(Path(transaction.backup_path), platforms):
                    print("✅ Rollback completed")
                else:
                    print("⚠ Rollback failed - manual intervention may be required")

            transaction.status = 'failed'
            transaction.error = str(e)
            self._save_transaction(transaction)

            return False

    def remove(self, platforms: List[str], keep_backup: bool = True) -> bool:
        """
        Atomically remove commands from specified platforms.

        Args:
            platforms: List of platform names
            keep_backup: Whether to keep backup after successful removal

        Returns:
            True if successful, False otherwise
        """
        print(f"🗑️ Starting atomic removal from platforms: {', '.join(platforms)}")

        # Validate platforms
        invalid_platforms = [p for p in platforms if p not in self.PLATFORMS]
        if invalid_platforms:
            print(f"❌ Invalid platforms: {', '.join(invalid_platforms)}")
            return False

        # Create transaction
        transaction = Transaction(
            id=self._generate_transaction_id(),
            operation='remove',
            platforms=platforms,
            timestamp=datetime.now().isoformat(),
            status='pending'
        )

        try:
            # Step 1: Backup existing state
            print("📦 Step 1: Creating backup...")
            backup_path = self._backup_commands(platforms)
            transaction.backup_path = str(backup_path)
            self._save_transaction(transaction)
            print(f"✅ Backup created: {backup_path}")

            # Step 2: Remove commands
            print("🗑️ Step 2: Removing commands...")
            for platform in platforms:
                commands_dir = self._get_platform_commands_dir(platform)

                if commands_dir.exists():
                    shutil.rmtree(commands_dir)
                    print(f"  ✓ Removed {platform} commands")

            # Step 3: Verify removal
            print("🔍 Step 3: Verifying removal...")
            for platform in platforms:
                commands_dir = self._get_platform_commands_dir(platform)
                if commands_dir.exists():
                    raise Exception(f"Verification failed: {platform} commands still exist")

            # Step 4: Mark transaction as completed
            transaction.status = 'completed'
            self._save_transaction(transaction)

            print(f"✅ Removal completed successfully!")
            print(f"Transaction ID: {transaction.id}")

            if keep_backup:
                print(f"💾 Backup preserved at: {backup_path}")

            return True

        except Exception as e:
            # Rollback on failure
            print(f"\n❌ Removal failed: {e}")
            print("🔄 Rolling back...")

            if transaction.backup_path:
                if self._restore_backup(Path(transaction.backup_path), platforms):
                    print("✅ Rollback completed")
                else:
                    print("⚠ Rollback failed - manual intervention may be required")

            transaction.status = 'failed'
            transaction.error = str(e)
            self._save_transaction(transaction)

            return False

    def rollback(self, transaction_id: str) -> bool:
        """Rollback a specific transaction"""
        print(f"🔄 Rolling back transaction: {transaction_id}")

        transaction = self._load_transaction(transaction_id)
        if not transaction:
            print(f"❌ Transaction not found: {transaction_id}")
            return False

        if transaction.status == 'rolled_back':
            print("⚠ Transaction already rolled back")
            return True

        if not transaction.backup_path:
            print("❌ No backup available for rollback")
            return False

        try:
            if self._restore_backup(Path(transaction.backup_path), transaction.platforms):
                transaction.status = 'rolled_back'
                self._save_transaction(transaction)
                print("✅ Rollback completed successfully")
                return True
            else:
                return False
        except Exception as e:
            print(f"❌ Rollback failed: {e}")
            return False

    def status(self):
        """Show status of all transactions"""
        print("\n📊 Transaction Status\n")

        transaction_files = sorted(self.transactions_dir.glob("*.json"), reverse=True)

        if not transaction_files:
            print("No transactions found")
            return

        for tf in transaction_files:
            with open(tf, 'r', encoding='utf-8') as f:
                data = json.load(f)
                transaction = Transaction(**data)

            status_icon = {
                'completed': '✅',
                'failed': '❌',
                'rolled_back': '🔄',
                'pending': '⏳'
            }.get(transaction.status, '❓')

            print(f"{status_icon} {transaction.id}")
            print(f"   Operation: {transaction.operation}")
            print(f"   Platforms: {', '.join(transaction.platforms)}")
            print(f"   Status: {transaction.status}")
            print(f"   Time: {transaction.timestamp}")

            if transaction.error:
                print(f"   Error: {transaction.error}")

            if transaction.backup_path:
                print(f"   Backup: {transaction.backup_path}")

            print()


def main():
    parser = argparse.ArgumentParser(
        description='DNASPEC CLI Command Manager - Atomic deployment/removal of CLI commands'
    )
    parser.add_argument(
        'action',
        choices=['deploy', 'remove', 'rollback', 'status'],
        help='Action to perform'
    )
    parser.add_argument(
        '--platforms',
        '-p',
        help='Comma-separated list of platforms (e.g., iflow,claude,copilot)'
    )
    parser.add_argument(
        '--source',
        '-s',
        help='Source directory for command templates'
    )
    parser.add_argument(
        '--transaction-id',
        '-t',
        help='Transaction ID (for rollback)'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not keep backup after successful removal'
    )

    args = parser.parse_args()

    # Get project root
    project_root = Path(__file__).parent.parent

    manager = CLICommandManager(project_root)

    if args.action == 'status':
        manager.status()

    elif args.action == 'deploy':
        if not args.platforms:
            print("❌ Error: --platforms is required for deploy")
            return 1

        platforms = [p.strip() for p in args.platforms.split(',')]
        source_dir = Path(args.source) if args.source else None

        success = manager.deploy(platforms, source_dir)
        return 0 if success else 1

    elif args.action == 'remove':
        if not args.platforms:
            print("❌ Error: --platforms is required for remove")
            return 1

        platforms = [p.strip() for p in args.platforms.split(',')]
        keep_backup = not args.no_backup

        success = manager.remove(platforms, keep_backup)
        return 0 if success else 1

    elif args.action == 'rollback':
        if not args.transaction_id:
            print("❌ Error: --transaction-id is required for rollback")
            return 1

        success = manager.rollback(args.transaction_id)
        return 0 if success else 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
