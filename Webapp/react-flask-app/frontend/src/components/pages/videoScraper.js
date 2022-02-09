import {Button, Col, Form, Row} from "react-bootstrap"

function VideoScraper() {
    return (
        <>
            <Row className={"pageContainer"}>
                <Col>
                    <Form>
                        <h2>Create Video Scraping Job</h2>
                        <Form.Group className="mb-3" controlId="formJob">
                            <Form.Label>Job Name</Form.Label>
                            <Form.Control type="text" placeholder="Enter job name"/>
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="formApi">
                            <Form.Label>API</Form.Label>
                            <Form.Select aria-label="Default select example">
                                <option>Select an API</option>
                                <option value="1">One</option>
                                <option value="2">Two</option>
                                <option value="3">Three</option>
                            </Form.Select>
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="formApi">
                            <Form.Label>Search Query</Form.Label>
                            <Form.Control type="text" placeholder="Enter a search query"/>
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="formApi">
                            <Form.Label>Published Before</Form.Label>
                            <Form.Control type="date" placeholder="Placeholder" id="dateSelectBefore"/>
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="formApi">
                            <Form.Label>Published After</Form.Label>
                            <Form.Control type="date" placeholder="Placeholder" id="dateSelectAfter"/>
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

export default VideoScraper
