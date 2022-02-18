import {Col, Row, Tab, Tabs} from "react-bootstrap"
import {A} from "hookrouter"
import {useCallback, useEffect, useState} from "react";
import axios from "axios";
import BootstrapTable from "react-bootstrap-table-next";

const columns = [
    {
        dataField: "name",
        text: "Name",
    },
    {
        dataField: "token",
        text: "Token",
    }
]

function ViewApis() {
    const [YouTubeApi, setYouTubeApi] = useState([])
    const [translationApi, setTranslationApi] = useState([])

    const host = window.location.href
    let host_ip = host.split(':')[1]
    const getApis = useCallback(() => {
        axios.get(`http://${host_ip}:1020/apis`)
            .then(response => {
                setYouTubeApi(response.data.filter(function (item) {
                    return item.service === "youtube"
                }))
                setTranslationApi(response.data.filter(function (item) {
                    return item.service === "g_translate"
                }))
            })
            .catch(error => {
                console.log(error)
            })
    }, [host_ip])

    useEffect(() => {
        const interval = setInterval(() => {
            getApis()
        }, 250)
        return () => clearInterval(interval)
    }, [getApis])

    const token = sessionStorage.getItem("access_token")
    if (token && token !== "" && token !== undefined) {
        return (
            <>
                <Row className={"pageContainer"}>
                    <Col>

                        <Tabs defaultActiveKey="youtube_apis" id="uncontrolled-tab-example" className="mb-3">
                            <Tab eventKey="youtube_apis" title="YouTube Apis">
                                <BootstrapTable keyField="id" data={YouTubeApi} columns={columns}/>
                            </Tab>
                            <Tab eventKey="translation_apis" title="Translation Apis">
                                <BootstrapTable keyField="id" data={translationApi} columns={columns}/>
                            </Tab>
                        </Tabs>
                    </Col>
                </Row>
            </>
        )
    } else {
        return (
            <>
                <Row className={"pageContainer"}>
                    <Col>
                        <p> 401 Unauthorized please login to view the content <A href="/">login</A>.</p>
                    </Col>
                </Row>
            </>
        )
    }
}

export default ViewApis