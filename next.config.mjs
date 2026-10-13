/** @type {import('next').NextConfig} */
const nextConfig = {
  turbopack: { root: process.cwd() },
  async rewrites() {
    const target = (
      process.env.FLASK_API_URL || "http://127.0.0.1:5200"
    ).replace(/\/$/, "");
    return [{ source: "/api/:path*", destination: `${target}/api/:path*` }];
  },
};

export default nextConfig;
