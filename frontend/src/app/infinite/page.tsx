"use client";

import { useInfiniteQuery } from "@tanstack/react-query";
import { pyconClient } from "~/openapi/pyconClient";

const fetchPage = async ({
	pageParam,
}: {
	pageParam?: string;
}) => {
	const response = await pyconClient.GET("/v2/users", {
		params: {
			query: {
				cursor: pageParam,
			},
		},
	});

	return {
		items: response.data?.items ?? [],
		cursor: response.data?.cursor,
	};
};

export default function HomePage() {
	const {
		data,
		isLoadingError,
		isLoading,
		fetchNextPage,
		hasNextPage,
		isFetchingNextPage,
	} = useInfiniteQuery({
		queryKey: ["users-v2"],
		queryFn: fetchPage,
		initialPageParam: undefined,
		getNextPageParam: (lastPage) => lastPage?.cursor,
	});

	if (isLoading) {
		return <div className="flex flex-col items-center">Loading...</div>;
	}

	if (isLoadingError || !data) {
		return <div>Error Page</div>;
	}

	return (
		<main className="flex flex-col gap-4 items-center">
			<h1 className="text-4xl">Users</h1>

			{data.pages.map((page) =>
				page?.items.map((user) => (
					<div
						key={user.id}
						className="flex w-96 flex-col gap-2 border border-neutral-600 p-4 rounded-lg bg-white shadow"
					>
						<h2 className="text-2xl font-medium">
							{user.family_name} {user.given_name}
						</h2>
						<p>{user.username}</p>
					</div>
				)),
			)}

			<div>
				<DataLoader
					isFetchingNextPage={isFetchingNextPage}
					fetchNextPage={fetchNextPage}
					hasNextPage={hasNextPage}
				/>
			</div>
		</main>
	);
}

function DataLoader({
	isFetchingNextPage,
	fetchNextPage,
	hasNextPage,
}: {
	isFetchingNextPage: boolean;
	fetchNextPage: () => void;
	hasNextPage: boolean;
}) {
	if (isFetchingNextPage) {
		return <span>Loading More...</span>;
	}

	if (hasNextPage) {
		return (
			<button
				type="button"
				onClick={() => {
					fetchNextPage();
				}}
			>
				Load More
			</button>
		);
	}

	return <span>End of List</span>;
}
