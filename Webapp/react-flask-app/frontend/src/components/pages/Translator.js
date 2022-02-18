import {Col, Row} from "react-bootstrap"
import {A} from "hookrouter"

function Translator() {
    const token = sessionStorage.getItem("access_token")
    if (token && token !== "" && token !== undefined) {
        return (
            <>
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

export default Translator