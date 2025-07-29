class stockMarketJobs():
    @staticmethod
    def create(step_id: int, step_name: str, step_desc: str):
        out = dict()
        out["step_id"] = step_id
        out["step_name"] = step_name
        out["step_desc"] = step_desc
        return out

def create_stock_market_job_list():
    jobs_list = []
    jobs_list.append(stockMarketJobs.create(1, "Get NSE APIs", "Prepare the list of NSE APIs"))
    jobs_list.append(stockMarketJobs.create(2, "Load Data From NSE APIs to MongoDB", "Load Data From NSE APIs to MongoDB"))
    return jobs_list

stock_market_job_list = create_stock_market_job_list()

if __name__ == "__main__":
    print(create_stock_market_job_list())