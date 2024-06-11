from flask import Flask, request, jsonify, render_template, render_template_string
import openai
import json

app = Flask(__name__)

# Set your OpenAI API key
openai.api_type = "azure"
openai.api_base = "https://imochaopenaipoc.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = "59ca414ba3ed425c991ae46cbe6e397d"


def get_completion(prompt, engine="gpt-35-turbo-16k-ContentTeam"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        engine=engine,
        messages=messages,
        temperature=0.5,
    )
    content = response.choices[0].message["content"]
    token_dict = {
        'prompt_tokens': response['usage']['prompt_tokens'],
        'completion_tokens': response['usage']['completion_tokens'],
        'total_tokens': response['usage']['total_tokens'],
    }
    print(f"Prompt Cost : {token_dict} ")
    return content


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_idp', methods=['POST'])
def generate_idp():
    data = request.json
    designation = data['designation']
    yoe = data['yoe']
    region = data['region']
    score_in_assessment = data['score_in_assessment']
    scored_good_in = data['scored_good_in']
    scored_bad_in = data['scored_bad_in']

    prompt_text = f"""
    An Individual Development Plan (IDP) is a structured approach utilized by Human Resources to assist employees in their career and personal development. 
    It is a personalized plan created in collaboration between the employee and their manager, detailing the employee's career goals, strengths, areas for improvement, and a timeline for achieving these objectives. 
    The IDP aims to align the employee's aspirations with the organization's goals, thereby fostering a culture of continuous learning and development.
    
    Inputs:-
        1. Designation: The job title of the employee.
        {designation}
        2. Years of Experience (YOE): The total number of years the employee has worked in their field.
        {yoe}
        3. Score in the Assessment: The result of the employee's recent performance evaluation.
        {score_in_assessment}
        4. Scored Good in: Areas where the employee has shown strong proficiency.
        {scored_good_in}
        5. Scored Bad in: Areas where the employee needs improvement.
        {scored_bad_in}
        6. Region: The geographical location of the employee.
        {region}
    
    Outputs:-
        1. Description of IDP for the Candidate: An overview of the IDP tailored to the specific employee.
        2. Strong Areas of the Candidate: Key strengths and proficiencies of the employee.
        3. Improvement Areas Needed for the Candidate: Skills and competencies where the employee needs development.
        4. 3/6/9-Month Development Plan for the Candidate: A structured timeline with actions and goals for improving behavioral, functional, technical, and positional skills, along with relevant training and certifications, career path.
    
    The JSON file should have the following key:value pair format:-
    {{
        description_of_idp: str,
        strong_areas: list
            strong_area_1: str
            strong_area_2: str
            ...
            strong_area_n: str
        improvement_areas: list
            improvement_area_1: str
            improvement_area_2: str
            ...
            improvement_area_n
        development_plan: dict
            3_months: dict
                behavioral_skills: dict
                    actions: list
                    goals: list
                functional_skills: dict
                    actions: list
                    goals: list
                technical_skills: dict
                    actions: list
                    goals: list
                positional_skills: dict
                    actions: list
                    goals: list
                training_certifications: dict
                    actions: list
                    goals: list
                career_path_and_job_role: dict
                    industry: list
                    job_roles: list
                    reason_for_job_transformation: list:str:provide 50 word job transformation description
            6_months: dict
                behavioral_skills: dict
                    actions: list
                    goals: list
                functional_skills: dict
                    actions: list
                    goals: list
                technical_skills: dict
                    actions: list
                    goals: list
                positional_skills: dict
                    actions: list
                    goals: list
                training_certifications: dict
                    actions: list
                    goals: list
                career_path_and_job_role: dict
                    industry: list
                    job_roles: list
                    reason_for_job_transformation: list:str:provide 50 word job transformation description
            9_months: dict
                behavioral_skills: dict
                    actions: list
                    goals: list
                functional_skills: dict
                    actions: list
                    goals: list
                technical_skills: dict
                    actions: list
                    goals: list
                positional_skills: dict
                    actions: list
                    goals: list
                training_certifications: dict
                    actions: list
                    goals: list
                career_path_and_job_role: dict
                    industry: list
                    job_roles: list
                    reason_for_job_transformation: list:str:provide 50 word job transformation description
    }}
    
    
    Instructions:-
        1. Review and Analyze: Begin by understanding the candidate's current role, experience, and performance assessment. Verify the candidate's strengths and areas for improvement based on their assessment scores.
        2. Evaluate Candidate's Skills: Identify and list the candidate’s strong areas. Determine and list the areas that need improvement.
        3. Develop the IDP: Outline a 3-month, 6-month, and 9-month development plan with specific actions and goals. The plan should cover: Behavioral Skills, Functional Skills, Technical Skills, Positional Skills, Training & Certifications, and Career Path.
        4. Use the Provided JSON Format: Fill in the JSON structure with the relevant details and goals for each period (3, 6, and 9 months).
    """

    generated_json = get_completion(prompt_text)

    with open("IDP.json", 'w') as file:
        file.write(generated_json)

    print("JSON file stored in IDP.json")

    generated_data = json.loads(generated_json)

    return jsonify(generated_data)


@app.route('/generate_html', methods=['POST'])
def generate_html():
    data = request.json
    description_of_idp = data['description_of_idp']
    strong_areas = data['strong_areas']
    improvement_areas = data['improvement_areas']
    development_plan = data['development_plan']

    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Individual Development Plan (IDP)</title>
    </head>
    <body>
        <h1>Individual Development Plan (IDP)</h1>

        <h2>Description of IDP:</h2>
        <p>{description_of_idp}</p>

        <h2>Strong Areas:</h2>
        <ul>
    '''
    for area in strong_areas:
        html_content += f'        <li>{area}</li>\n'
    html_content += '''
        </ul>

        <h2>Improvement Areas:</h2>
        <ul>
    '''
    for area in improvement_areas:
        html_content += f'        <li>{area}</li>\n'
    html_content += '''
        </ul>

        <h2>Development Plan:</h2>
    '''
    for timeframe, skills in development_plan.items():
        html_content += f'    <h3>{timeframe.capitalize()} Development Plan</h3>\n'
        html_content += '    <ul>\n'
        for skill_type, details in skills.items():
            html_content += f'        <li>{skill_type.capitalize().replace("_", " ")}:</li>\n'
            html_content += '        <ul>\n'
            for action_goal, values in details.items():
                html_content += f'            <li>{action_goal.capitalize()}:</li>\n'
                html_content += '            <ul>\n'
                for item in values:
                    html_content += f'                <li>{item}</li>\n'
                html_content += '            </ul>\n'
            html_content += '        </ul>\n'
        html_content += '    </ul>\n'
    html_content += '''
    </body>
    </html>
    '''

    return render_template_string(html_content)


if __name__ == '__main__':
    app.run(debug=True)
