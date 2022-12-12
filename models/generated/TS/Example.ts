import { z } from "zod"
import { createOption, createOptionSchema, Option, None } from "../../../Option"
 import { ExampleSubType, ExampleSubTypeSchema } from "./ExampleSubType"

export class Example {
    string_prop?: string = ""
    string_optional_prop?: string 
    int_with_mod_prop?: number 
    int_prop: number 
    boolean_prop: boolean 
    option_string_prop: Option<string> 
    url_prop: string 
    http_url_prop: string 
    float_prop: number 
    string_array_prop: string[] 
    int_array_1_prop: number[] 
    int_array_2_prop: number[] 
    complex_array: ExampleSubType[] 
    date_prop: string 

    constructor(init: z.infer<typeof ExampleSchema>) {
        
        this.string_prop = init.string_prop
        this.string_optional_prop = init.string_optional_prop
        this.int_with_mod_prop = init.int_with_mod_prop
        this.int_prop = init.int_prop
        this.boolean_prop = init.boolean_prop
        this.option_string_prop = createOption(init.option_string_prop, false, z.string().min(5))
        this.url_prop = init.url_prop
        this.http_url_prop = init.http_url_prop
        this.float_prop = init.float_prop
        this.string_array_prop = init.string_array_prop
        this.int_array_1_prop = init.int_array_1_prop
        this.int_array_2_prop = init.int_array_2_prop
        this.complex_array = init.complex_array
        this.date_prop = init.date_prop
    }

    static fromJSON(parsedJSON: any) {
        const validated = ExampleSchema.parse(parsedJSON)
        return new Example(validated)
    }
}

export const ExampleSchema = z.object({
    string_prop: z.string().min(5).optional(),
    string_optional_prop: z.string().optional(),
    int_with_mod_prop: z.number().int().gt(10).optional(),
    int_prop: z.number().int(),
    boolean_prop: z.boolean(),
    option_string_prop: createOptionSchema(z.string().min(5)),
    url_prop: z.string().url(),
    http_url_prop: z.string().url(),
    float_prop: z.number().lte(12),
    string_array_prop: z.string().array(),
    int_array_1_prop: z.number().int().array(),
    int_array_2_prop: z.number().int().array(),
    complex_array: ExampleSubTypeSchema.array(),
    date_prop: z.date(),
})