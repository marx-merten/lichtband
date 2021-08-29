import {  browser, dev } from '$app/env';

function getBaseUrl(){
    if (dev) return "http://172.17.100.43/"
    else return "/"
}

export function fetch_api<T>(url:string):Promise<T>{
    if (browser)
        return fetch(getBaseUrl()+url).then(response =>{
            if (!response.ok) {
                throw new Error(response.statusText)
            }
            return response.json()
        })
    else return new Promise( (result)=>result(null))
}