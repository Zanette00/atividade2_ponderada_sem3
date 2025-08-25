import pandas as pd


def calculate_demographic_data(print_data: bool = True):
    # Carregar os dados a partir do arquivo
    df = pd.read_csv("adult.data.csv")

    # Quantas pessoas de cada raça estão representadas neste conjunto?
    # Deve ser uma Series do Pandas com os nomes das raças como índice.
    race_count = df["race"].value_counts()

    # Qual é a idade média dos homens?
    average_age_men = round(df[df["sex"] == "Male"]["age"].mean(), 1)

    # Qual a porcentagem de pessoas com bacharelado?
    percentage_bachelors = round(
        (df[df["education"] == "Bachelors"].shape[0] / df.shape[0]) * 100, 1
    )

    # Qual a porcentagem de pessoas com ensino avançado (Bacharelado, Mestrado ou Doutorado)
    # que ganham mais de 50K?
    # E qual a porcentagem sem ensino avançado que ganham mais de 50K?
    higher_education_mask = df["education"].isin(["Bachelors", "Masters", "Doctorate"])
    lower_education_mask = ~higher_education_mask

    # porcentagem com salário >50K
    higher_education_rich = round(
        (df[higher_education_mask & (df["salary"] == ">50K")].shape[0]
         / df[higher_education_mask].shape[0]) * 100,
        1,
    )
    lower_education_rich = round(
        (df[lower_education_mask & (df["salary"] == ">50K")].shape[0]
         / df[lower_education_mask].shape[0]) * 100,
        1,
    )

    # Qual é o mínimo de horas trabalhadas por semana (coluna hours-per-week)?
    min_work_hours = int(df["hours-per-week"].min())

    # Entre quem trabalha o mínimo de horas, qual a porcentagem com salário >50K?
    num_min_workers = df[df["hours-per-week"] == min_work_hours]
    rich_percentage = round(
        ((num_min_workers["salary"] == ">50K").sum() / len(num_min_workers)) * 100,
        0,
    )

    # Qual país tem a maior proporção de pessoas que ganham >50K?
    country_salary_share = (
        df.groupby("native-country")["salary"].value_counts(normalize=True).unstack(fill_value=0)
    )
    highest_earning_country_percentage = round((country_salary_share[">50K"] * 100).max(), 1)
    highest_earning_country = (country_salary_share[">50K"] * 100).idxmax()

    # Ocupação mais frequente entre quem ganha >50K na Índia.
    top_IN_occupation = (
        df[(df["native-country"] == "India") & (df["salary"] == ">50K")]["occupation"].value_counts().idxmax()
        if not df[(df["native-country"] == "India") & (df["salary"] == ">50K")].empty
        else None
    )

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(
            f"Highest percentage of rich people in country: {highest_earning_country_percentage}%"
        )
        print("Top occupations in India:", top_IN_occupation)

    return {
        "race_count": race_count,
        "average_age_men": average_age_men,
        "percentage_bachelors": percentage_bachelors,
        "higher_education_rich": higher_education_rich,
        "lower_education_rich": lower_education_rich,
        "min_work_hours": min_work_hours,
        "rich_percentage": rich_percentage,
        "highest_earning_country": highest_earning_country,
        "highest_earning_country_percentage": highest_earning_country_percentage,
        "top_IN_occupation": top_IN_occupation,
    }


