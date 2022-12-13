import { z } from "zod"
import { createOption, createOptionSchema, Option, None } from "../../Option"

export class ExampleSubType {
    string_prop: string 

    constructor(init: z.infer<typeof ExampleSubTypeSchema>) {
        
        this.string_prop = init.string_prop
    }

    static fromJSON(parsedJSON: any) {
        const validated = ExampleSubTypeSchema.parse(parsedJSON)
        return new ExampleSubType(validated)
    }

    static getSchema() {
        return ExampleSubTypeSchema
    }
}

export const ExampleSubTypeSchema = z.object({
    string_prop: z.string(),
})