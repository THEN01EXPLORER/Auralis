import * as vscode from 'vscode';
import { Vulnerability } from './analyzer';

export class DiagnosticsManager {
    private diagnosticCollection: vscode.DiagnosticCollection;

    constructor() {
        this.diagnosticCollection = vscode.languages.createDiagnosticCollection('auralis');
    }

    updateDiagnostics(uri: vscode.Uri, vulnerabilities: Vulnerability[]) {
        const diagnostics: vscode.Diagnostic[] = vulnerabilities.map(vuln => {
            const line = Math.max(0, vuln.line - 1);
            const range = new vscode.Range(line, 0, line, 1000);
            
            const diagnostic = new vscode.Diagnostic(
                range,
                `${vuln.type}: ${vuln.description}`,
                this.getSeverity(vuln.severity)
            );

            diagnostic.source = 'Auralis';
            diagnostic.code = vuln.type;
            
            // Add code actions for fixes
            if (vuln.remediation) {
                diagnostic.relatedInformation = [
                    new vscode.DiagnosticRelatedInformation(
                        new vscode.Location(uri, range),
                        `Fix: ${vuln.remediation.explanation}`
                    )
                ];
            }

            return diagnostic;
        });

        this.diagnosticCollection.set(uri, diagnostics);
    }

    private getSeverity(severity: string): vscode.DiagnosticSeverity {
        switch (severity.toLowerCase()) {
            case 'critical':
            case 'high':
                return vscode.DiagnosticSeverity.Error;
            case 'medium':
                return vscode.DiagnosticSeverity.Warning;
            case 'low':
                return vscode.DiagnosticSeverity.Information;
            default:
                return vscode.DiagnosticSeverity.Hint;
        }
    }

    clear(uri: vscode.Uri) {
        this.diagnosticCollection.delete(uri);
    }

    dispose() {
        this.diagnosticCollection.dispose();
    }
}
