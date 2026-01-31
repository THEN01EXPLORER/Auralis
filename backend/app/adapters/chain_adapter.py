"""
Multi-Chain Adapter Interface
Provides a unified interface for analyzing contracts across different blockchains
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from enum import Enum

class ChainType(Enum):
    """Supported blockchain types"""
    ETHEREUM = "ethereum"
    SOLANA = "solana"
    MOVE_APTOS = "move_aptos"
    MOVE_SUI = "move_sui"

class ChainAdapter(ABC):
    """Abstract base class for blockchain-specific analyzers"""
    
    @abstractmethod
    def get_chain_type(self) -> ChainType:
        """Return the blockchain type this adapter handles"""
        pass
    
    @abstractmethod
    def validate_code(self, code: str) -> bool:
        """Validate if the code is valid for this blockchain"""
        pass
    
    @abstractmethod
    def analyze(self, code: str) -> Dict:
        """
        Analyze smart contract code
        
        Returns:
            Dict with vulnerabilities in Auralis format
        """
        pass
    
    @abstractmethod
    def get_language(self) -> str:
        """Return the programming language (e.g., 'solidity', 'rust', 'move')"""
        pass


class EthereumAdapter(ChainAdapter):
    """Adapter for Ethereum/EVM-compatible chains (Solidity)"""
    
    def get_chain_type(self) -> ChainType:
        return ChainType.ETHEREUM
    
    def get_language(self) -> str:
        return "solidity"
    
    def validate_code(self, code: str) -> bool:
        """Check if code looks like Solidity"""
        solidity_keywords = ['pragma solidity', 'contract ', 'function ', 'modifier ']
        return any(keyword in code for keyword in solidity_keywords)
    
    def analyze(self, code: str) -> Dict:
        """
        Analyze Solidity code using existing Auralis pipeline
        This is the default implementation - actual analysis happens in orchestrator
        """
        return {
            'chain_type': self.get_chain_type().value,
            'language': self.get_language(),
            'supported': True
        }


class SolanaAdapter(ChainAdapter):
    """Adapter for Solana (Rust)"""
    
    def get_chain_type(self) -> ChainType:
        return ChainType.SOLANA
    
    def get_language(self) -> str:
        return "rust"
    
    def validate_code(self, code: str) -> bool:
        """Check if code looks like Solana Rust"""
        solana_keywords = ['use solana_program', 'entrypoint!', 'ProgramResult', 'AccountInfo']
        return any(keyword in code for keyword in solana_keywords)
    
    def analyze(self, code: str) -> Dict:
        """
        Analyze Solana Rust code
        TODO: Implement Solana-specific analysis (post-MVP)
        """
        return {
            'chain_type': self.get_chain_type().value,
            'language': self.get_language(),
            'supported': False,
            'message': 'Solana analysis coming soon in post-MVP release'
        }


class MoveAptosAdapter(ChainAdapter):
    """Adapter for Aptos (Move)"""
    
    def get_chain_type(self) -> ChainType:
        return ChainType.MOVE_APTOS
    
    def get_language(self) -> str:
        return "move"
    
    def validate_code(self, code: str) -> bool:
        """Check if code looks like Move"""
        move_keywords = ['module ', 'public entry fun', 'use aptos_framework', 'acquires']
        return any(keyword in code for keyword in move_keywords)
    
    def analyze(self, code: str) -> Dict:
        """
        Analyze Aptos Move code
        TODO: Implement Move-specific analysis (post-MVP)
        """
        return {
            'chain_type': self.get_chain_type().value,
            'language': self.get_language(),
            'supported': False,
            'message': 'Aptos Move analysis coming soon in post-MVP release'
        }


class MoveSuiAdapter(ChainAdapter):
    """Adapter for Sui (Move)"""
    
    def get_chain_type(self) -> ChainType:
        return ChainType.MOVE_SUI
    
    def get_language(self) -> str:
        return "move"
    
    def validate_code(self, code: str) -> bool:
        """Check if code looks like Sui Move"""
        sui_keywords = ['module ', 'public entry fun', 'use sui::', 'TxContext']
        return any(keyword in code for keyword in sui_keywords)
    
    def analyze(self, code: str) -> Dict:
        """
        Analyze Sui Move code
        TODO: Implement Sui-specific analysis (post-MVP)
        """
        return {
            'chain_type': self.get_chain_type().value,
            'language': self.get_language(),
            'supported': False,
            'message': 'Sui Move analysis coming soon in post-MVP release'
        }


class ChainAdapterFactory:
    """Factory for creating appropriate chain adapters"""
    
    def __init__(self):
        self.adapters = [
            EthereumAdapter(),
            SolanaAdapter(),
            MoveAptosAdapter(),
            MoveSuiAdapter()
        ]
    
    def detect_chain(self, code: str) -> Optional[ChainAdapter]:
        """
        Auto-detect which blockchain the code is for
        
        Returns:
            Appropriate ChainAdapter or None if not detected
        """
        for adapter in self.adapters:
            if adapter.validate_code(code):
                return adapter
        
        # Default to Ethereum if no match
        return self.adapters[0]
    
    def get_adapter(self, chain_type: ChainType) -> Optional[ChainAdapter]:
        """Get adapter for specific chain type"""
        for adapter in self.adapters:
            if adapter.get_chain_type() == chain_type:
                return adapter
        return None
    
    def list_supported_chains(self) -> List[Dict]:
        """List all supported chains and their status"""
        return [
            {
                'chain': adapter.get_chain_type().value,
                'language': adapter.get_language(),
                'supported': adapter.get_chain_type() == ChainType.ETHEREUM
            }
            for adapter in self.adapters
        ]
