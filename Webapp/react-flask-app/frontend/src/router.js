import React from "react"
import Login from "./components/pages/Login"
import Home from "./components/pages/Home"
import VideoScraper from "./components/pages/VideoScraper"
import CommentScraper from "./components/pages/CommentScraper"
import Translator from "./components/pages/Translator"
import CreateApi from "./components/pages/CreateApi"
import ViewApis from "./components/pages/ViewApis"


const routes = {
    "/": () => <Login/>,
    "/home": () => <Home/>,
    "/createvideojob": () => <VideoScraper/>,
    "/createcommentjob": () => <CommentScraper/>,
    "/translator": () => <Translator/>,
    "/createapi": () => <CreateApi/>,
    "/viewapis": () => <ViewApis/>
}

export default routes