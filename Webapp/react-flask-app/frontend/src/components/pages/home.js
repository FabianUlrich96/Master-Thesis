import axios from "axios"
import BootstrapTable from "react-bootstrap-table-next"
import {Col, Row, Tab, Tabs} from "react-bootstrap"
import {useEffect, useState, useCallback} from "react"


    const columns = [
        {
            dataField: "name",
            text: "Name",
        },
        {
            dataField: "query",
            text: "Query",
        },
        {
            dataField: "api",
            text: "Api",
        },
        {
            dataField: "date",
            text: "Date"
        },
        {
            dataField: "state",
            text: "State"
        }
    ]

    function Home() {
        const [videoJob, setVideoJob] = useState([])
        const [commentJob, setCommentJob] = useState([])
        const [translationJob, setTranslationJob] = useState([])
        const host = window.location.href
        let host_ip = host.split(':')[1]

        const getJobs = useCallback(() => {
            axios.get(`http://${host_ip}:1020/jobs`)
                .then(response => {
                    setCommentJob(response.data.filter(function(item) {
                        return item.job_type === "comment"
                    }))
                    setVideoJob(response.data.filter(function(item) {
                        return item.job_type === "video"
                    }))
                    setTranslationJob(response.data.filter(function(item) {
                        return item.job_type === "translation"
                    }))
                })
                .catch(error => {
                    console.log(error)
                })
        }, [host_ip])
        
        useEffect(() => {
            const interval = setInterval(() => {
                getJobs()
            }, 250)
            return () => clearInterval(interval)
        }, [getJobs])

    return (
        <>
            <Row className={"pageContainer"}>
                <Col>

                    <Tabs defaultActiveKey="video_scraping_jobs" id="uncontrolled-tab-example" className="mb-3">
                        <Tab eventKey="video_scraping_jobs" title="Video Jobs">
                            <BootstrapTable keyField="id" data={videoJob} columns={columns} />
                        </Tab>
                        <Tab eventKey="comment_scraping_jobs" title="Comment Jobs">
                            <BootstrapTable keyField="id" data={commentJob} columns={columns} />
                        </Tab>
                        <Tab eventKey="translator_jobs" title="Translator Jobs">
                            <BootstrapTable keyField="id" data={translationJob} columns={columns} />
                        </Tab>
                    </Tabs>
                </Col>
            </Row>
        </>
    )
}

export default Home

