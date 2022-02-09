import {Button, Col, Form, Row} from "react-bootstrap"
import axios from "axios"
import {useState} from "react"

function CreateApi() {
    const host = window.location.href
    let host_ip = host.split(':')[1]
    const [name, setName] = useState()
    const [token, setToken] = useState()
    const [service, setService] = useState()


    function onSubmit(values) {
        values.preventDefault()
        let data = {
            name: name,
            token: token,
            service: service
        }

        console.log(data)

        axios.post(`http://${host_ip}:1020/apis`, data).then(async res => {
            if (res.status === 200) {
                console.log(res.status)
            } else {
                console.log(res.status)
            }
        })
    }

    return (
        <>
            <Row className={"pageContainer"}>
                <Col>
                    <Form onSubmit={onSubmit}>
                        <h2>Add API</h2>
                        <Form.Group className="mb-3" controlId="formName">
                            <Form.Label>API Name</Form.Label>
                            <Form.Control type="text" placeholder="Enter API Name"
                                          onChange={e => setName(e.target.value)}/>
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="formToken">
                            <Form.Label>API Token</Form.Label>
                            <Form.Control type="text" placeholder="Enter API Token"
                                          onChange={e => setToken(e.target.value)}/>
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="formService">
                            <Form.Label>Service Name</Form.Label>
                            <Form.Select aria-label="Default select example" onChange={e => setService(e.target.value)}>
                                <option>Select a Service</option>
                                <option value="g_translate">Google Translate</option>
                                <option value="youtube">YouTube</option>
                            </Form.Select>
                        </Form.Group>

                        <Button variant="primary" type="submit">
                            Submit
                        </Button>
                    </Form>
                </Col>
            </Row>
        </>
    )
}

export default CreateApi