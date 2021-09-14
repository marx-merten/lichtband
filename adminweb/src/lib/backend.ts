import {writable} from 'svelte/store'
import { fetch_api } from '$lib/servercalls'
class RGBValue{
    constructor(public red:number,public green:number, public blue:number){}
}
class LightState{
    state = false
    rgb=new RGBValue(0,0,0)
    currentScene=""
    scenes:string[]=[]
    sceneActive:false

    public static from_json(data:any) :LightState{
        const ls = new LightState()
        ls.currentScene = data.activeScene
        ls.state = data.state
        ls.scenes=data.scenes
        ls.rgb.red = data.rgb[0]
        ls.rgb.green = data.rgb[1]
        ls.rgb.blue = data.rgb[2]
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