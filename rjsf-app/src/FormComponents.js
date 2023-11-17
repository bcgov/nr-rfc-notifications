import Form from "@rjsf/core";
import React from "react";
import validator from '@rjsf/validator-ajv8';


function FormComponent() {
    const schema = require("./form/schema.json")
    const formData = require("./form/rules.json")
    const uiSchema = require("./form/uiSchema.json")


    return (
        <div className="form">
            <Form
                schema={schema}
                uiSchema={uiSchema}
                formData={formData}
                validator={validator}
            >

            </Form>
        </div>
    )
}

export default FormComponent