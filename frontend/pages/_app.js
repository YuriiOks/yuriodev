import Layout from '../components/Layout';
import '../styles/globals.css'; // Import global styles
import { AuthProvider } from '../contexts/AuthContext'; // Import AuthProvider

function MyApp({ Component, pageProps }) {
  // You can pass page-specific layout props here if needed
  // For example, different titles for different pages
  const pageTitle = Component.title || "Yuri Oliveira - Portfolio";

  return (
    <AuthProvider>
      <Layout title={pageTitle}>
        <Component {...pageProps} />
      </Layout>
    </AuthProvider>
  );
}

export default MyApp;
