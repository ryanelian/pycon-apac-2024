import createClient from "openapi-fetch";
import type { paths, components } from "./pycon";

export type PythonClientTypes = components; 

export const pyconClient = createClient<paths>({
	baseUrl: "/fastapi/",
});

import type { Middleware } from "openapi-fetch";

/**
 * Safely tries to get the response body as JSON or text.
 */
async function tryGetResponseBody(response: Response): Promise<unknown> {
	try {
		return response.headers.get("content-type")?.includes("json")
			? await response.clone().json()
			: await response.clone().text();
	} catch {
		return "(Failed to parse response body)";
	}
}

/**
 * Middleware to throw an error if the response status code is 4xx or 5xx.
 * This is required for react-query to handle errors correctly.
 *
 * @see https://github.com/openapi-ts/openapi-typescript/blob/main/packages/openapi-fetch/examples/react-query/src/lib/api/index.ts
 */
export const throwOnErrorMiddleware: Middleware = {
	async onResponse({ response }) {
		if (response.status >= 400) {
			const body = await tryGetResponseBody(response);
			throw new DetailedApiError(response.status, response.statusText, body);
		}
		return undefined;
	},
};

class DetailedApiError extends Error {
	constructor(
		public status: number,
		public statusText: string,
		public body: unknown,
	) {
		super(`HTTP ${status}: ${statusText}`);
	}
}

pyconClient.use(throwOnErrorMiddleware);
