import axios from 'axios';

export interface Vulnerability {
    type: string;
    line: number;
    severity: 'Critical' | 'High' | 'Medium' | 'Low';
    confidence: number;
    description: string;
    recommendation: string;
    remediation?: {
        explanation: string;
        code_example: string;
    };
}

export interface AnalysisResult {
    analysis_id: string;
    risk_score: number;
    vulnerabilities: Vulnerability[];
    summary: string;
    analysis_method: 'static' | 'ai' | 'hybrid';
    ai_available: boolean;
    processing_time_ms: number;
}

export class AuralisAnalyzer {
    constructor(private apiEndpoint: string) {}

    async analyzeContract(code: string): Promise<AnalysisResult> {
        try {
            const response = await axios.post<AnalysisResult>(
                `${this.apiEndpoint}/api/v1/analyze`,
                { code },
                { timeout: 30000 }
            );
            return response.data;
        } catch (error: any) {
            if (error.response) {
                throw new Error(`API Error: ${error.response.status} - ${error.response.data?.detail || 'Unknown error'}`);
            } else if (error.request) {
                throw new Error('Cannot connect to Auralis API. Please check if the backend is running.');
            } else {
                throw new Error(`Analysis failed: ${error.message}`);
            }
        }
    }

    async analyzeWithSlither(code: string, filePath: string): Promise<any> {
        // Placeholder for Slither integration
        // This will be implemented when Slither is set up
        return null;
    }
}
