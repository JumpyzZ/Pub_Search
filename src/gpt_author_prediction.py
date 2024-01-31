from openai import OpenAI
import os

client = OpenAI(api_key="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")


def get_prediction_score(description, abstract) -> float:

    # # Generate response from GPT-3.5
    # response = openai.Completion.create(
    #     engine="gpt-3.5-turbo",
    #     prompt=prompt,
    #     temperature=0.5,
    #     max_tokens=50,
    #     n=1,
    #     stop=None
    # )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You must give and only givr a 0-10 prediction score(like 8.5, 7.7, 1.5 ONLY THE PREDICTION SCORE), given abstract and researcher intro, to decide wether a papper in written by this researcher"},
            {"role": "user", "content": f"Researcher Description: {description} Abstract: {abstract}"}
        ],
        temperature=0.5
    )

    try:
        prediction_score = float(response.choices[0].message.content)
    except ValueError:
        prediction_score = -1

    return prediction_score


def main():
    # Example usage
    description = 'Michael is an Associate Professor in Engineering Science at the University of Auckland who specialises in Operations Research (OR). After completing a degree in Mathematics and Computer Science and a Masters in OR at the University of Auckland, Michael spent time at Stanford University in the US where he obtained a MS in Engineering-Economic Systems and OR, and a PhD in Management Science and Engineering. Michael created the research group Operations Research Union Analytics (ORUA) which combines OR and analytics to develop intelligent systems'
    abstract = 'In some geothermal systems there are high concentrations of chloride and some non-condensible gas (mainly CO2). For reservoir modelling, equation of state (EOS) modules that can handle non-isothermal mixtures of water, chloride and NCGs are required. In the TOUGH2 simulator, EWASG provides a suitable EOS. In this paper we describe a set of new EOS modules for modelling chloride-rich systems using the parallel, opensource geothermal flow simulator Waiwera. EOS modules for water & chloride, water, chloride & CO2 and water, chloride & air are provided. Shared code is used to give consistency between results from different EOS modules. The main physical properties of chloride are computed using the updated thermodynamic formulation of Driesner (2007) which also removes the low-temperature limitations of EWASG. As in the pure water and water & NCG EOS modules for Waiwera, primary variable interpolation gives improved phase transition performance and hence faster convergence of natural state simulations. Some results for theoretical test problems and real high- and low-temperature geothermal fields are presented. Keywords: Reservoir models, numerical modelling, flow simulator, Waiwera, chloride, non-condensible gas'

    prediction_score = get_prediction_score(description, abstract)
    print("Prediction Score:", prediction_score)


if __name__ == '__main__':
    main()
