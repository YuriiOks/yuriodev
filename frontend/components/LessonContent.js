import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import styles from '../styles/LessonContent.module.css'; // Create this CSS module
import CodeSandbox from './CodeSandbox'; // Import the CodeSandbox component

// Optional: Add syntax highlighting for code blocks
// import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
// import { dracula } from 'react-syntax-highlighter/dist/cjs/styles/prism'; // Choose a style

// const CodeBlock = ({ node, inline, className, children, ...props }) => {
//   const match = /language-(\w+)/.exec(className || '');
//   return !inline && match ? (
//     <SyntaxHighlighter
//       style={dracula} // Your chosen style
//       language={match[1]}
//       PreTag="div"
//       {...props}
//     >
//       {String(children).replace(/\n$/, '')}
//     </SyntaxHighlighter>
//   ) : (
//     <code className={className} {...props}>
//       {children}
//     </code>
//   );
// };

const LessonContent = ({ lesson }) => {
  if (!lesson) {
    return <div className={styles.loading}>Loading lesson content...</div>;
  }

  switch (lesson.content_type) {
    case 'TEXT':
    case 'text': // Handle potential casing differences
      if (!lesson.content_text) {
        return <div className={styles.noContent}>No text content available for this lesson.</div>;
      }
      return (
        <div className={styles.markdownContainer}>
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            // components={{ code: CodeBlock }} // For syntax highlighting
          >
            {lesson.content_text}
          </ReactMarkdown>
        </div>
      );
    case 'VIDEO':
    case 'video':
      return (
        <div className={styles.placeholder}>
          <h4>Video Content Placeholder</h4>
          {lesson.content_path ? (
            <p>Video source: {lesson.content_path}</p>
          ) : (
            <p>No video path provided.</p>
          )}
          {/* Future: Embed video player here based on content_path */}
        </div>
      );
    case 'QUIZ':
    case 'quiz':
      return (
        <div className={styles.placeholder}>
          <h4>Quiz Placeholder</h4>
          {lesson.content_path && <p>Quiz ID/Path: {lesson.content_path}</p>}
          {/* Future: Embed quiz component here */}
        </div>
      );
    case 'CODE_SANDBOX':
    case 'code_sandbox':
      // The CodeSandbox component can take initialCode as a prop.
      // We can use lesson.content_text to store the initial Python code for the sandbox.
      return <CodeSandbox initialCode={lesson.content_text || ''} />;
    default:
      return <div className={styles.error}>Unsupported lesson content type: {lesson.content_type}</div>;
  }
};

export default LessonContent;
