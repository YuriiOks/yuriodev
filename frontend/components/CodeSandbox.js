import React, { useState, useEffect } from 'react';
import Editor from 'react-simple-code-editor';
import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-python'; // Language support for Python
import 'prismjs/themes/prism-tomorrow.css'; // Choose a PrismJS theme
import styles from '../styles/CodeSandbox.module.css'; // Create this CSS module
import { executeCode } from '../services/sandboxService'; // Create this service

const CodeSandbox = ({ initialCode = '' }) => {
  const [code, setCode] = useState(initialCode);
  const [output, setOutput] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [executionResult, setExecutionResult] = useState(null);


  const handleRunCode = async () => {
    setIsLoading(true);
    setOutput('');
    setError('');
    setExecutionResult(null);
    try {
      const result = await executeCode(code);
      setExecutionResult(result);
      if (result.success) {
        setOutput(result.output);
        if(result.error) { // Store stderr even if successful for informational purposes
            setError(`Standard Error:\n${result.error}`);
        }
      } else {
        setOutput(result.output || ''); // Show output even if error
        setError(result.error || 'Code execution failed.');
      }
    } catch (err) {
      console.error("executeCode service error:", err);
      setError(err.message || 'An error occurred while communicating with the execution service.');
    } finally {
      setIsLoading(false);
    }
  };

  // Highlight function for PrismJS
  const highlightWithPrism = (code) => highlight(code, languages.python, 'python');

  return (
    <div className={styles.sandboxContainer}>
      <h4>Python Code Sandbox</h4>
      <div className={styles.editorContainer}>
        <Editor
          value={code}
          onValueChange={newCode => setCode(newCode)}
          highlight={highlightWithPrism}
          padding={10}
          style={{
            fontFamily: '"Fira code", "Fira Mono", monospace',
            fontSize: 14,
            border: '1px solid #ddd',
            borderRadius: '4px',
            minHeight: '150px',
          }}
          textareaClassName={styles.editorTextarea} // For further specific styling if needed
        />
      </div>
      <button onClick={handleRunCode} disabled={isLoading} className={`button ${styles.runButton}`}>
        {isLoading ? 'Running...' : 'Run Code'}
      </button>

      {executionResult && (
        <div className={styles.resultsContainer}>
            <h5>Results:</h5>
            {output && (
                <div className={styles.outputSection}>
                    <h6>Output (stdout):</h6>
                    <pre className={styles.outputPre}>{output}</pre>
                </div>
            )}
            {error && ( // Display error from stderr or execution error
                <div className={styles.errorSection}>
                    <h6>Error (stderr / execution):</h6>
                    <pre className={`${styles.outputPre} ${styles.errorPre}`}>{error}</pre>
                </div>
            )}
            {executionResult.execution_time !== undefined && (
                 <p className={styles.executionTime}>Execution time: {executionResult.execution_time}s</p>
            )}
             {executionResult.exit_code !== undefined && executionResult.exit_code !== null && (
                 <p className={styles.exitCode}>Exit Code: {executionResult.exit_code}</p>
            )}
        </div>
      )}
    </div>
  );
};

export default CodeSandbox;
