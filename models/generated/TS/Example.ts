import { z } from "zod"
import { createOption, createOptionSchema, Option, None } from "../../../Option"

export class Example {
    string_prop?: string = ""
    int_with_mod_prop?: number 
    int_prop: number 
    boolean_prop: boolean 
    option_string_prop: Option<string> 
    url_prop: string 
    http_url_prop: string 
    float_prop: number 

    constructor(init: z.infer<typeof ExampleSchema>) {
        
        this.string_prop = init.string_prop
        this.int_with_mod_prop = init.int_with_mod_prop
        this.int_prop = init.int_prop
        this.boolean_prop = init.boolean_prop
        this.option_string_prop = createOption(init.option_string_prop, false, z.string().min(5))
        this.url_prop = init.url_prop
        this.http_url_prop = init.http_url_prop
        this.float_prop = init.float_prop
    }

    static fromJSON(parsedJSON: any) {
        const validated = ExampleSchema.parse(parsedJSON)
        return new Example(validated)
    }
}

export const ExampleSchema = z.object({
    string_prop: z.string().min(5).optional(),
    int_with_mod_prop: z.number().int().gt(10).optional(),
    int_prop: z.number().int(),
    boolean_prop: z.boolean(),
    option_string_prop: createOptionSchema(z.string().min(5)),
    url_prop: z.string().url(),
    http_url_prop: z.string().url(),
    float_prop: z.number().lte(12),
})