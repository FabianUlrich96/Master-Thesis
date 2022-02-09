import {Button, Col, Form, Row} from "react-bootstrap"

function CommentScraper() {
    return (
        <>
            <Row className={"pageContainer"}>
                <Col>
                    <Form>
                        <h2>Create Comment Scraping Job</h2>
                        <Form.Group className="mb-3" controlId="formApi">
                            <Form.Label>Video Job</Form.Label>
                            <Form.Select aria-label="Default select example">
                                <option>Select a video job</option>
                                <option value="1">One</option>
                                <option value="2">Two</option>
                                <option value="3">Three</option>
                            </Form.Select>
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
                        <Button variant="primary" type="submit">
                            Submit
                        </Button>
                    </Form>
                </Col>
            </Row>
        </>
    )
}

export default CommentScraper
