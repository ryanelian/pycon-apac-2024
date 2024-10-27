export function toErrorMessage(error: unknown) {
	if (error instanceof Error) {
		return error.message;
	}

	if (typeof error === "string") {
		return error;
	}

	return JSON.stringify(error);
}
