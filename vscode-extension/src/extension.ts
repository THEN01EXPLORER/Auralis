import * as vscode from 'vscode';
import { AuralisAnalyzer } from './analyzer';
import { VulnerabilityTreeProvider } from './vulnerabilityTree';
import { DiagnosticsManager } from './diagnostics';
import { ControlFlowGraphProvider } from './controlFlowGraph';

let analyzer: AuralisAnalyzer;
let diagnosticsManager: DiagnosticsManager;
let vulnerabilityTreeProvider: VulnerabilityTreeProvider;

export function activate(context: vscode.ExtensionContext) {
    console.log('Auralis extension is now active');

    // Initialize components
    const config = vscode.workspace.getConfiguration('auralis');
    const apiEndpoint = config.get<string>('apiEndpoint', 'http://localhost:8000');
    
    analyzer = new AuralisAnalyzer(apiEndpoint);
    diagnosticsManager = new DiagnosticsManager();
    vulnerabilityTreeProvider = new VulnerabilityTreeProvider();

    // Register tree view
    vscode.window.registerTreeDataProvider('auralisVulnerabilities', vulnerabilityTreeProvider);

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('auralis.analyzeContract', analyzeCurrentContract)
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('auralis.showVulnerabilityTree', () => {
            vscode.commands.executeCommand('workbench.view.extension.auralisVulnerabilities');
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('auralis.showControlFlowGraph', showControlFlowGraph)
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('auralis.applyFix', applyFix)
    );

    // Auto-analyze on save if enabled
    context.subscriptions.push(
        vscode.workspace.onDidSaveTextDocument(async (document) => {
            const enableRealTime = config.get<boolean>('enableRealTimeAnalysis', true);
            if (enableRealTime && document.languageId === 'solidity') {
                await analyzeDocument(document);
            }
        })
    );

    // Show welcome message
    vscode.window.showInformationMessage('Auralis Security Auditor activated! 🛡️');
}

async function analyzeCurrentContract() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor found');
        return;
    }

    if (editor.document.languageId !== 'solidity') {
        vscode.window.showWarningMessage('Auralis only supports Solidity files (.sol)');
        return;
    }

    await analyzeDocument(editor.document);
}

async function analyzeDocument(document: vscode.TextDocument) {
    const code = document.getText();
    
    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: 'Auralis: Analyzing contract...',
        cancellable: false
    }, async () => {
        try {
            const result = await analyzer.analyzeContract(code);
            
            // Update diagnostics
            diagnosticsManager.updateDiagnostics(document.uri, result.vulnerabilities);
            
            // Update vulnerability tree
            vulnerabilityTreeProvider.updateVulnerabilities(document.uri, result);
            
            // Show summary
            const vulnCount = result.vulnerabilities.length;
            const message = vulnCount > 0 
                ? `Found ${vulnCount} vulnerabilities (Risk Score: ${result.risk_score})`
                : 'No vulnerabilities found ✓';
            
            vscode.window.showInformationMessage(`Auralis: ${message}`);
            
        } catch (error: any) {
            vscode.window.showErrorMessage(`Auralis analysis failed: ${error.message}`);
        }
    });
}

async function showControlFlowGraph() {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.document.languageId !== 'solidity') {
        vscode.window.showWarningMessage('Open a Solidity file to view control flow graph');
        return;
    }

    const panel = vscode.window.createWebviewPanel(
        'auralisControlFlow',
        'Auralis: Control Flow Graph',
        vscode.ViewColumn.Beside,
        { enableScripts: true }
    );

    const provider = new ControlFlowGraphProvider();
    panel.webview.html = provider.getWebviewContent(editor.document.getText());
}

async function applyFix(vulnerability: any) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        return;
    }

    // Apply the fix suggestion
    const edit = new vscode.WorkspaceEdit();
    const line = vulnerability.line - 1;
    const range = editor.document.lineAt(line).range;
    
    if (vulnerability.remediation?.code_example) {
        edit.replace(editor.document.uri, range, vulnerability.remediation.code_example);
        await vscode.workspace.applyEdit(edit);
        vscode.window.showInformationMessage('Fix applied successfully!');
    }
}

export function deactivate() {
    diagnosticsManager?.dispose();
}
