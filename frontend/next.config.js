/**
 * Run `build` or `dev` with `SKIP_ENV_VALIDATION` to skip env validation. This is especially useful
 * for Docker builds.
 */
await import("./src/env.js");

/** @type {import("next").NextConfig} */
const config = {
	async rewrites() {
		return [
			{
				source: "/fastapi/:path*",
				destination: "http://localhost:8000/:path*",
			},
		];
	},
};

export default config;
