import React from "react"
import Login from "./components/pages/login"
import Home from "./components/pages/home"
import VideoScraper from "./components/pages/videoScraper"
import CommentScraper from "./components/pages/commentScraper"
import Translator from "./components/pages/translator"
import CreateApi from "./components/pages/CreateApi"
import ViewApis from "./components/pages/viewApis"


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