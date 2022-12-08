import { z } from "zod"
import { createOption, createOptionSchema, Option, None } from "../../Option/Option"
import {BaseModel} from "../common";
 import { Umgebung, UmgebungSchema } from "./Umgebung"

export class Example extends BaseModel {
    string_prop?: string = ""
    int_prop?: number 
    boolean_prop: boolean 
    option_string_prop: Option<string> 
    umgebung_prop: Umgebung 

    constructor(
        {string_prop,int_prop,boolean_prop,option_string_prop,umgebung_prop} :
        {string_prop?:string,int_prop?:number,boolean_prop:boolean,option_string_prop:Option<string>,umgebung_prop:Umgebung}
    ) {
        super()
        if (string_prop) {
            this.string_prop = string_prop
        }
        this.int_prop = int_prop
        this.boolean_prop = boolean_prop
        this.option_string_prop = option_string_prop
        this.umgebung_prop = umgebung_prop
    }

    static fromJSON(parsedJSON: any) {
        const validated = ExampleSchema.parse(parsedJSON)
        return new Example({
            string_prop: validated.string_prop,
            int_prop: validated.int_prop,
            boolean_prop: validated.boolean_prop,
            option_string_prop: createOption(validated.option_string_prop, false, z.string().min(5)),
            umgebung_prop: validated.umgebung_prop,
        })
    }
}

export const ExampleSchema = z.object({
    string_prop: z.string().min(5).optional(),
    int_prop: z.number().int().gt(10).optional(),
    boolean_prop: z.boolean(),
    option_string_prop: createOptionSchema(z.string().min(5)),
    umgebung_prop: UmgebungSchema,
})