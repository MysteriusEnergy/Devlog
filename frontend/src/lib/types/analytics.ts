export type ProjectBreakdownItem = {
	project_id: string;
	total_minutes: number;
};

export type AnalyticsSummary = {
	total_minutes: number;
	total_hours: number;
	weekly_minutes: number;
	project_breakdown: ProjectBreakdownItem[];
};
