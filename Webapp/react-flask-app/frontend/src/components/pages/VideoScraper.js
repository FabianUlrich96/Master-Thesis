import {Button, Col, Form, Row} from "react-bootstrap"
import {useCallback, useEffect, useState} from "react"
import axios from "axios"
import {A, navigate} from "hookrouter"

function VideoScraper() {
    const host = window.location.href
    let host_ip = host.split(':')[1]
    const [apisDatabase, setApisDatabase] = useState([])
    const [ form, setForm ] = useState({})
    const [ errors, setErrors ] = useState({})

    const loadAPIs = useCallback(() => {
        axios.get(`http://${host_ip}:1020/apis`).then((response) => {
            console.log(response.data)
            const apis = []
            const result_data = response.data
            result_data.forEach(api => {
                apis.push({
                    rendered: <option key={api.name}>{api.name}</option>,
                    service: api.service
                })
            })
            setApisDatabase(apis)
        }).catch(error => {
            console.log(error)
        })


    }, [host_ip])



    const setField = (field, value) => {
        setForm({
            ...form,
            [field]: value
        })

        if ( !!errors[field] ) setErrors({
            ...errors,
            [field]: null
        })
    }
    const findFormErrors = () => {
        const { name, api, query, published_before, published_after } = form
        const newErrors = {}
        // name errors
        if ( !name || name === '' ) newErrors.name = 'cannot be blank!'
        else if ( name.length > 30 ) newErrors.name = 'name is too long!'
        // api errors
        if ( !api || api === '' ) newErrors.api = 'select an api!'
        // query errors
        if ( !query || query === '' ) newErrors.query = 'cannot be blank!'
        // published_before errors
        if ( !published_before || published_before === '' ) newErrors.published_before = 'cannot be blank!'
        // published_after errors
        if ( !published_after || published_after === '' ) newErrors.published_after = 'cannot be blank!'

        return newErrors
    }

    function onSubmit(values) {
        console.log(values)
        console.log(errors)
        values.preventDefault()
        const newErrors = findFormErrors()
        if ( Object.keys(newErrors).length > 0 ) {
            // We got errors!
            setErrors(newErrors)
        } else {
            let data = {
                name: form.name,
                api: form.api,
                query: form.query,
                published_before: form.published_before,
                published_after: form.published_after,
                job_type: "video"
            }

            console.log(data)

            axios.post(`http://${host_ip}:1020/jobs`, data).then(async res => {
                if (res.status === 200) {
                    console.log(res.status)
                } else {
                    console.log(res.status)
                }
            })
            navigate('/home')
        }

    }

    useEffect(() => {
        loadAPIs()
    }, [loadAPIs])

    const token = sessionStorage.getItem("access_token")
    if (token && token !== "" && token !== undefined) {
        return (
            <>
                <Row className={"pageContainer"}>
                    <Col>
                        <Form onSubmit={onSubmit}>
                            <h2>Create Video Scraping Job</h2>
                            <Form.Group className="mb-3">
                                <Form.Label>Job Name</Form.Label>
                                <Form.Control type="text" placeholder="Enter job name"
                                              onChange={ e => setField('name', e.target.value) }
                                              isInvalid={!!errors.name} />
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label>API</Form.Label>

                                <Form.Control as='select' onChange={ e => setField('api', e.target.value) }
                                              isInvalid={!!errors.api}
                                >
                                    <option value=''>Select an api:</option>
                                    {apisDatabase.filter(option => option.service === "youtube").map(option => option.rendered)}
                                </Form.Control>

                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label>Search Query</Form.Label>
                                <Form.Control type="text" placeholder="Enter a search query"
                                              onChange={ e => setField('query', e.target.value) }
                                              isInvalid={!!errors.query} />
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label>Published Before</Form.Label>
                                <Form.Control type="date" placeholder="Placeholder" id="dateSelectBefore"
                                              onChange={ e => setField('published_before', e.target.value) }
                                              isInvalid={!!errors.published_before} />
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label>Published After</Form.Label>
                                <Form.Control type="date" placeholder="Placeholder" id="dateSelectAfter"
                                              onChange={ e => setField('published_after', e.target.value) }
                                              isInvalid={!!errors.published_after} />
                            </Form.Group>


                            <Button variant="primary" type="submit">
                                Submit
                            </Button>
                        </Form>
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

export default VideoScraper
