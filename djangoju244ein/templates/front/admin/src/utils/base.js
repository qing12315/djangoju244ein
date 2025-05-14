const base = {
    get() {
        return {
            url : "http://localhost:8080/djangoju244ein/",
            name: "djangoju244ein",
            // 退出到首页链接
            indexUrl: ''
        };
    },
    getProjectName(){
        return {
            projectName: "高校就业分析与可视化系统"
        } 
    }
}
export default base
