export type Project = {
	id: string;
	name: string;
	description: string;
	color: string;
	created_at: string;
	updated_at: string;
};

export type CreateProjectRequest = {
	name: string;
	description?: string;
	color: string;
};

export type UpdateProjectRequest = {
	name?: string;
	description?: string;
	color?: string;
};
