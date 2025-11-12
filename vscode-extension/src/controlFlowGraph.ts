export class ControlFlowGraphProvider {
    getWebviewContent(code: string): string {
        // Parse contract for functions and calls
        const functions = this.extractFunctions(code);
        const nodes = this.generateNodes(functions);
        const edges = this.generateEdges(code, functions);

        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Control Flow Graph</title>
    <script src="https://cdn.jsdelivr.net/npm/vis-network@9.1.2/dist/vis-network.min.js"></script>
    <style>
        body { margin: 0; padding: 0; font-family: Arial, sans-serif; }
        #graph { width: 100%; height: 100vh; border: 1px solid #ddd; }
        .legend {
            position: absolute;
            top: 10px;
            right: 10px;
            background: white;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        .legend-item { margin: 5px 0; }
        .legend-color { 
            display: inline-block; 
            width: 20px; 
            height: 20px; 
            margin-right: 5px; 
            vertical-align: middle;
        }
    </style>
</head>
<body>
    <div class="legend">
        <div class="legend-item">
            <span class="legend-color" style="background: #97C2FC;"></span>
            <span>Function</span>
        </div>
        <div class="legend-item">
            <span class="legend-color" style="background: #FB7E81;"></span>
            <span>External Call</span>
        </div>
        <div class="legend-item">
            <span class="legend-color" style="background: #FFA807;"></span>
            <span>State Change</span>
        </div>
    </div>
    <div id="graph"></div>
    <script>
        const nodes = new vis.DataSet(${JSON.stringify(nodes)});
        const edges = new vis.DataSet(${JSON.stringify(edges)});
        
        const container = document.getElementById('graph');
        const data = { nodes, edges };
        const options = {
            nodes: {
                shape: 'box',
                margin: 10,
                font: { size: 14 }
            },
            edges: {
                arrows: 'to',
                smooth: { type: 'cubicBezier' }
            },
            physics: {
                enabled: true,
                barnesHut: {
                    gravitationalConstant: -2000,
                    springLength: 150
                }
            }
        };
        
        const network = new vis.Network(container, data, options);
        
        network.on('click', function(params) {
            if (params.nodes.length > 0) {
                const nodeId = params.nodes[0];
                const node = nodes.get(nodeId);
                alert('Function: ' + node.label + '\\nLine: ' + node.line);
            }
        });
    </script>
</body>
</html>`;
    }

    private extractFunctions(code: string): Array<{name: string, line: number}> {
        const functions: Array<{name: string, line: number}> = [];
        const lines = code.split('\n');
        
        lines.forEach((line, index) => {
            const match = line.match(/function\s+(\w+)/);
            if (match) {
                functions.push({
                    name: match[1],
                    line: index + 1
                });
            }
        });

        return functions;
    }

    private generateNodes(functions: Array<{name: string, line: number}>) {
        return functions.map((func, index) => ({
            id: index,
            label: func.name,
            line: func.line,
            color: '#97C2FC'
        }));
    }

    private generateEdges(code: string, functions: Array<{name: string, line: number}>) {
        const edges: Array<{from: number, to: number}> = [];
        const lines = code.split('\n');
        
        functions.forEach((func, fromIndex) => {
            // Find function calls within this function
            functions.forEach((targetFunc, toIndex) => {
                if (fromIndex !== toIndex) {
                    const funcRegex = new RegExp(`\\b${targetFunc.name}\\s*\\(`);
                    if (funcRegex.test(code)) {
                        edges.push({ from: fromIndex, to: toIndex });
                    }
                }
            });
        });

        return edges;
    }
}
