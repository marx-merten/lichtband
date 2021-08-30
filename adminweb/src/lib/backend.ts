import {writable} from 'svelte/store'
import { fetch_api } from '$lib/servercalls'
class RGBWValue{
    constructor(public red:number,public green:number, public blue:number, public white:number){}
}
class LightState{
    state = false
    rgbw=new RGBWValue(0,0,0,0)
    currentScene=""
    scenes:string[]=[]
    sceneActive:false

    public static from_json(data:any) :LightState{
        const ls = new LightState()
        ls.currentScene = data.activeScene
        ls.state = data.state
        ls.scenes=data.scenes
        ls.rgbw.red = data.rgbw[0]
        ls.rgbw.green = data.rgbw[1]
        ls.rgbw.blue = data.rgbw[2]
        ls.rgbw.white = data.rgbw[3]
        ls.sceneActive=data.sceneState
        return ls
    }
}

export const lightState = writable(new LightState())

export function fetch_light_state():void{
    fetch_api('api/light/status').then((state: any) => {
        lightState.set(LightState.from_json(state))
    });
}