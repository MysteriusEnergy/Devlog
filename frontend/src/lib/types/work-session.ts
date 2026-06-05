export type WorkSession = {
	id: string;
	project_id: string;
	date: string;
	start_time: string;
	end_time: string;
	duration_minutes: number;
	notes: string;
	created_at: string;
	updated_at: string;
};

export type CreateWorkSessionRequest = {
	project_id: string;
	date: string;
	start_time: string;
	end_time: string;
	notes?: string;
};

export type UpdateWorkSessionRequest = {
	start_time?: string;
	end_time?: string;
	notes?: string;
};

export type WorkSessionsResponse = {
	data: WorkSession[];
	pagination: {
		page: number;
		per_page: number;
		total: number;
		total_pages: number;
	};
};

export type WorkSessionsFilters = {
	project_id?: string;
	date?: string;
	from?: string;
	to?: string;
	page?: number;
	per_page?: number;
};
