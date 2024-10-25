"use client";

import { useQuery } from "@tanstack/react-query";
import { pyconClient } from "~/openapi/pyconClient";
import { toErrorMessage } from "~/components/toErrorMessage";

export default function HomePage() {
	const { data, isLoadingError, error, isLoading } = useQuery({
		queryKey: ["users"],
		queryFn: async () => {
			const response = await pyconClient.GET("/v1/users");
			return response.data;
		},
	});

	const users = data ?? [];

	return (
		<main className="flex flex-col gap-4">
			<h1 className="text-4xl">Users</h1>
			{isLoading && <p>Loading...</p>}
			{isLoadingError ? <p>{toErrorMessage(error)}</p> : null}

			{users.map((user) => (
				<div key={user.id} className="flex flex-col gap-1">
					<h2>{user.username}</h2>
					<p>
						{user.family_name} {user.given_name}
					</p>
				</div>
			))}
		</main>
	);
}
