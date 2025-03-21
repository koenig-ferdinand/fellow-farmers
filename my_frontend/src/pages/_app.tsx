import type { AppProps } from "next/app";
import "@/styles/index.css"; // Tailwind + custom styles

function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}

export default MyApp;
