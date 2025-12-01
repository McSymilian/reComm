import {useState, useRef, useEffect, createContext} from "react";

export const WebsocketContext = createContext(
    false, null, () => {})


export const WebsocketProvider = ({ children }) => {
    const [isReady, setIsReady] = useState(false)
    const [val, setVal] = useState(null)

    const ws = useRef(null)

    useEffect(() => {
        const socket = new WebSocket("ws://127.0.0.1:8000")

        socket.onopen = () => setIsReady(true)
        socket.onclose = () => setIsReady(false)
        socket.onmessage = (event) => setVal(event.data)

        ws.current = socket

        return () => {
            socket.close()
        }
    }, [])

    const ret = [isReady, val, ws.current?.send.bind(ws.current)]

    return (
        <WebsocketContext.Provider value={ret}>
            {children}
        </WebsocketContext.Provider>
    )
}