import Layout from '../components/Layout';
import '../styles/globals.css'; // Import global styles

function MyApp({ Component, pageProps }) {
  // You can pass page-specific layout props here if needed
  // For example, different titles for different pages
  const pageTitle = Component.title || "Yuri Oliveira - Portfolio";

  return (
    <Layout title={pageTitle}>
      <Component {...pageProps} />
    </Layout>
  );
}

export default MyApp;
