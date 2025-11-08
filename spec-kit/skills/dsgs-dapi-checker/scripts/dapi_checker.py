"""
DSGS Distributed API Documentation Checker Script
Implements the core functionality for checking interface consistency across system components
"""

import re
from typing import Dict, Any, List, Tuple
from enum import Enum


class InterfaceType(Enum):
    API = "api"
    DATA = "data"
    COMMUNICATION = "communication"
    INTERNAL = "internal"


class Interface:
    def __init__(self, name: str, interface_type: InterfaceType, 
                 definition: str, implementation: str = ""):
        self.name = name
        self.type = interface_type
        self.definition = definition
        self.implementation = implementation
        self.issues = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type.value,
            "definition": self.definition,
            "implementation": self.implementation,
            "issues": self.issues
        }


class DAPIChecker:
    def __init__(self):
        self.api_pattern = r'/[a-zA-Z0-9/_-]+'
        self.param_pattern = r'\{[a-zA-Z0-9_-]+\}|\[[a-zA-Z0-9_-]+\]'
        self.method_pattern = r'(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)'
        
    def extract_apis(self, text: str) -> List[Dict[str, str]]:
        """Extract API endpoints from text"""
        apis = []
        
        # Find lines that look like API definitions
        lines = text.split('\n')
        for line in lines:
            # Look for lines with HTTP methods and endpoints
            method_match = re.search(self.method_pattern, line, re.IGNORECASE)
            endpoint_match = re.search(self.api_pattern, line)
            
            if method_match and endpoint_match:
                api_info = {
                    'method': method_match.group().upper(),
                    'endpoint': endpoint_match.group(),
                    'full_line': line.strip()
                }
                
                # Extract parameters
                params = re.findall(self.param_pattern, line)
                api_info['parameters'] = params
                
                apis.append(api_info)
        
        return apis
    
    def extract_data_interfaces(self, text: str) -> List[Dict[str, str]]:
        """Extract data interface definitions (schemas, formats)"""
        data_interfaces = []
        
        # Look for schema-like definitions
        schema_patterns = [
            r'@?schema\s+([a-zA-Z0-9_]+)',
            r'data\s+type\s+([a-zA-Z0-9_]+)',
            r'format:\s*([a-zA-Z0-9_]+)',
            r'type:\s*([a-zA-Z0-9_]+)'
        ]
        
        for pattern in schema_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                data_interfaces.append({
                    'name': match,
                    'definition': f"Data interface for {match}",
                    'type': 'schema'
                })
        
        # Look for JSON-like structures
        json_blocks = re.findall(r'\{[^}]*\}', text)
        for block in json_blocks:
            # Extract field names from JSON structure
            fields = re.findall(r'"([a-zA-Z0-9_]+)"', block)
            if fields:
                data_interfaces.append({
                    'name': f"DataStructure_{len(data_interfaces)}",
                    'definition': f"JSON structure with fields: {', '.join(fields)}",
                    'type': 'data_structure'
                })
        
        return data_interfaces
    
    def extract_communication_interfaces(self, text: str) -> List[Dict[str, str]]:
        """Extract communication interface definitions"""
        comm_interfaces = []
        
        # Look for communication protocol definitions
        protocol_patterns = [
            r'protocol:\s*([a-zA-Z0-9_]+)',
            r'message\s+format:\s*([a-zA-Z0-9_]+)',
            r'communication\s+type:\s*([a-zA-Z0-9_]+)',
            r'amqp|mqtt|kafka|tcp|udp|http|websocket|grpc'
        ]
        
        for pattern in protocol_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                comm_interfaces.append({
                    'name': f"Communication_{match}",
                    'definition': f"Communication interface using {match}",
                    'type': 'protocol'
                })
        
        return comm_interfaces
    
    def check_api_consistency(self, api_defs: List[Dict], api_impls: List[Dict]) -> List[str]:
        """Check consistency between API definitions and implementations"""
        issues = []
        
        # Create sets of defined and implemented endpoints for comparison
        defined_endpoints = {(api['method'], api['endpoint']) for api in api_defs}
        implemented_endpoints = {(api['method'], api['endpoint']) for api in api_impls}
        
        # Find missing implementations
        missing_impl = defined_endpoints - implemented_endpoints
        for method, endpoint in missing_impl:
            issues.append(f"Missing implementation for {method} {endpoint} (defined but not implemented)")
        
        # Find extra implementations
        extra_impl = implemented_endpoints - defined_endpoints
        for method, endpoint in extra_impl:
            issues.append(f"Extra implementation for {method} {endpoint} (implemented but not defined)")
        
        # Check parameter consistency if available
        for def_api in api_defs:
            for impl_api in api_impls:
                if (def_api['method'], def_api['endpoint']) == (impl_api['method'], impl_api['endpoint']):
                    def_params = set(def_api.get('parameters', []))
                    impl_params = set(impl_api.get('parameters', []))
                    
                    missing_params = def_params - impl_params
                    if missing_params:
                        issues.append(f"Missing parameters in implementation for {def_api['method']} {def_api['endpoint']}: {missing_params}")
                    
                    extra_params = impl_params - def_params
                    if extra_params:
                        issues.append(f"Extra parameters in implementation for {def_api['method']} {def_api['endpoint']}: {extra_params}")
        
        return issues
    
    def check_data_consistency(self, data_defs: List[Dict], data_impls: List[Dict]) -> List[str]:
        """Check consistency between data definitions and implementations"""
        issues = []
        
        # Simple comparison - in a real implementation this would be more sophisticated
        for definition in data_defs:
            found = False
            for implementation in data_impls:
                if definition['name'] == implementation['name']:
                    found = True
                    break
            if not found:
                issues.append(f"Data definition '{definition['name']}' has no corresponding implementation")
        
        return issues
    
    def check_communication_consistency(self, comm_defs: List[Dict], comm_impls: List[Dict]) -> List[str]:
        """Check consistency between communication definitions and implementations"""
        issues = []
        
        for definition in comm_defs:
            found = False
            for implementation in comm_impls:
                if definition['name'].lower() == implementation['name'].lower():
                    found = True
                    break
            if not found:
                issues.append(f"Communication definition '{definition['name']}' has no corresponding implementation")
        
        return issues
    
    def check_consistency(self, documentation: str, implementation: str) -> Dict[str, Any]:
        """Check consistency between documentation and implementation"""
        # Extract interfaces from both documentation and implementation
        doc_apis = self.extract_apis(documentation)
        impl_apis = self.extract_apis(implementation)
        
        doc_data = self.extract_data_interfaces(documentation)
        impl_data = self.extract_data_interfaces(implementation)
        
        doc_comm = self.extract_communication_interfaces(documentation)
        impl_comm = self.extract_communication_interfaces(implementation)
        
        # Check consistency for each interface type
        api_issues = self.check_api_consistency(doc_apis, impl_apis)
        data_issues = self.check_data_consistency(doc_data, impl_data)
        comm_issues = self.check_communication_consistency(doc_comm, impl_comm)
        
        # Compile results
        results = {
            "documentation_analyzed": len(documentation),
            "implementation_analyzed": len(implementation),
            "interface_counts": {
                "documented_apis": len(doc_apis),
                "implemented_apis": len(impl_apis),
                "documented_data": len(doc_data),
                "implemented_data": len(impl_data),
                "documented_comm": len(doc_comm),
                "implemented_comm": len(impl_comm)
            },
            "consistency_issues": {
                "api_issues": api_issues,
                "data_issues": data_issues,
                "communication_issues": comm_issues
            },
            "total_issues": len(api_issues) + len(data_issues) + len(comm_issues),
            "summary": {
                "api_consistency": "OK" if not api_issues else f"{len(api_issues)} issues found",
                "data_consistency": "OK" if not data_issues else f"{len(data_issues)} issues found",
                "communication_consistency": "OK" if not comm_issues else f"{len(comm_issues)} issues found"
            }
        }
        
        return results
    
    def generate_consistency_report(self, documentation: str, implementation: str) -> Dict[str, Any]:
        """Generate a comprehensive consistency report"""
        consistency_results = self.check_consistency(documentation, implementation)
        
        # Calculate consistency score
        total_interfaces = (consistency_results["interface_counts"]["documented_apis"] + 
                           consistency_results["interface_counts"]["documented_data"] + 
                           consistency_results["interface_counts"]["documented_comm"])
        
        score = 0
        if total_interfaces > 0:
            score = max(0, 100 * (total_interfaces - consistency_results["total_issues"]) / total_interfaces)
        
        consistency_results["consistency_score"] = round(score, 2)
        
        return consistency_results


def main():
    """
    Example usage of the DAPIChecker
    """
    documentation = """
    Here are the API endpoints defined for the user management service:
    
    GET /users - Retrieve all users
    POST /users - Create a new user with {username}, {email}, {password}
    GET /users/{id} - Retrieve a specific user
    PUT /users/{id} - Update a specific user with {name}, {email}
    DELETE /users/{id} - Delete a specific user
    
    Data Format: All data should be in JSON format with fields user_id, name, email, created_date.
    Communication Protocol: Use HTTP for API calls and JSON for data exchange.
    """
    
    implementation = """
    // API Implementation
    app.get('/users', UserController.getAllUsers);
    app.post('/users', UserController.createUser); 
    app.get('/users/:id', UserController.getUser);  // Changed to :id from {id}
    app.put('/users/:id', UserController.updateUser);  // Changed to :id from {id}
    // app.delete('/users/:id', UserController.deleteUser);  // This endpoint is commented out
    
    // Data handling
    const UserSchema = {
        user_id: Number,
        name: String,
        email: String,
        created_date: Date
    };
    
    // Communication implementation using HTTP
    const httpClient = require('axios');
    """
    
    checker = DAPIChecker()
    report = checker.generate_consistency_report(documentation, implementation)
    
    print("## DAPI Consistency Check Report")
    print(f"Consistency Score: {report['consistency_score']}/100")
    print(f"Total Issues Found: {report['total_issues']}")
    
    print("\n### Interface Counts:")
    for interface_type, count in report['interface_counts'].items():
        print(f"- {interface_type}: {count}")
    
    print("\n### Summary:")
    for category, status in report['summary'].items():
        print(f"- {category}: {status}")
    
    print("\n### Detailed Issues:")
    for category, issues in report['consistency_issues'].items():
        if issues:
            print(f"\n**{category}**:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"  No {category} issues found")


if __name__ == "__main__":
    main()