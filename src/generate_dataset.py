import csv
from pathlib import Path


def build_name_dataset(output_path: Path) -> None:
    """Build a CSV dataset of Indian first names and write it to disk."""
    male_names = [
        "Aarav", "Aditya", "Arjun", "Rohan", "Siddharth", "Karan", "Rahul", "Aakash",
        "Vikram", "Arnav", "Dev", "Kunal", "Rajat", "Saurabh", "Manish", "Amit",
        "Vivek", "Mohan", "Anil", "Pranav", "Harsh", "Nikhil", "Sahil", "Rakesh",
        "Vijay", "Ajay", "Deepak", "Ravi", "Pankaj", "Sandeep", "Gautam", "Shubham",
        "Ritesh", "Tanish", "Naveen", "Ashish", "Kishore", "Prashant", "Ankit", "Pradeep",
        "Sandeep", "Nilesh", "Yash", "Tarun", "Aman", "Rupesh", "Alok", "Kamal",
        "Pranay", "Mayank", "Dinesh", "Sujit", "Kartik", "Jay", "Akhil", "Ishan",
        "Samir", "Abhinav", "Vikash", "Krishna", "Arvind", "Anup", "Bhavesh", "Pulkit",
        "Raghav", "Amitabh", "Vishal", "Kabir", "Samar", "Uday", "Nitin", "Shreyas",
        "Rupak", "Shaurya", "Tushar", "Vimal", "Adarsh", "Anish", "Bharat", "Chirag",
        "Dheeraj", "Eshan", "Farhan", "Gaurav", "Himanshu", "Inder", "Jatin", "Keshav",
        "Lokesh", "Madhav", "Nikhilesh", "Ojas", "Parth", "Quamar", "Ritesh", "Samarjeet",
        "Tejas", "Uttam", "Vijendra", "Waseem", "Xavier", "Yashwant", "Zubin", "Aayush",
        "Bharath", "Chandan", "Darshan", "Eklavya", "Firoz", "Giriraj", "Hardeep", "Irfan",
        "Jeevan", "Kalyan", "Lalit", "Manav", "Niraj", "Omesh", "Prithvi", "Qasim",
        "Rajeev", "Saket", "Tarakesh", "Umesh", "Vasant", "Wahid", "Yogesh", "Zahir",
        "Aarush", "Bimal", "Chetan", "Dhruv", "Ekagra", "Fateh", "Girish", "Harish",
        "Ishaan", "Jagdish", "Kumar", "Lakshya", "Mahesh", "Nandan", "Omkar", "Pavan",
        "Ravindra", "Subhash", "Trilok", "Utkarsh", "Vijayraj", "Yuvraj", "Zeeshan", "Ashwin",
        "Bhuvan", "Chetan", "Darsh", "Eshwar", "Faizal", "Ganesh", "Hrithik", "Imran",
        "Jayant", "Kabir", "Laxman", "Milan", "Nikhilesh", "Ojaswin", "Pravin", "Rohit",
        "Sameer", "Tapan", "Ujjwal", "Vijayendra", "Yogendra", "Adarsh", "Bhupen", "Chiranjiv",
        "Debasis", "Eklavya", "Faraz", "Gopal", "Hitesh", "Ismail", "Jatin", "Karanjit",
        "Lokendra", "Maulik", "Nimish", "Paritosh", "Ravikant", "Srinivas", "Tanmay", "Udayan",
        "Viren", "Yashpal", "Zeeshan", "Arpit", "Bijay", "Chandan", "Dilip", "Eshaan",
        "Fardeen", "Gautam", "Hemant", "Ishwar", "Jashan", "Kartikeya", "Lalit", "Mayur",
        "Niranjan", "Omprakash", "Pritam", "Ranjit", "Sujay", "Tushar", "Utsav", "Vijendra",
        "Yogesh", "Abhay", "Bharat", "Charan", "Deepak", "Eshwar", "Faiz", "Gaurang",
        "Harmeet", "Imtiyaz", "Jayesh", "Krish", "Lakshman", "Mihir", "Nikunj", "Prajwal",
        "Rupesh", "Shailesh", "Tarun", "Vishesh", "Yatin"
    ]
    female_names = [
        "Aanya", "Aditi", "Ananya", "Anika", "Anjali", "Sneha", "Priya", "Sonal",
        "Neha", "Pooja", "Shreya", "Riya", "Isha", "Shruti", "Shikha", "Divya",
        "Meera", "Kavya", "Nikita", "Aishwarya", "Sakshi", "Natasha", "Prerna", "Radhika",
        "Tanvi", "Vidya", "Preeti", "Madhuri", "Anushka", "Bhavna", "Deepika", "Esha",
        "Farah", "Geeta", "Hina", "Ira", "Janhvi", "Kiran", "Laxmi", "Manisha",
        "Nisha", "Ojasvi", "Parul", "Rashmi", "Sangeeta", "Tanya", "Usha", "Vaishali",
        "Yogita", "Zara", "Akanksha", "Bhumika", "Charu", "Deeksha", "Eshani", "Falguni",
        "Gauri", "Himani", "Ila", "Jaya", "Kavita", "Leena", "Monika", "Nandini",
        "Pallavi", "Ritika", "Sana", "Trisha", "Urmi", "Vandana", "Yamini", "Zeenat",
        "Aarohi", "Bela", "Chetna", "Diksha", "Eesha", "Fiza", "Gitanjali", "Hiral",
        "Ipsita", "Juhi", "Kajal", "Latika", "Mansi", "Neelam", "Ojaswini", "Poonam",
        "Rhea", "Shivani", "Tara", "Urvashi", "Vani", "Yamini", "Zoya", "Asha",
        "Bina", "Chandni", "Damini", "Ekta", "Fariha", "Ganga", "Hardika", "Ila",
        "Jagruti", "Kiran", "Lalita", "Megha", "Nimita", "Palak", "Rachna", "Sanya",
        "Trupti", "Usha", "Veda", "Yamini", "Aanchal", "Bharti", "Chaitali", "Diya",
        "Esha", "Femida", "Gayatri", "Hansa", "Indira", "Jaya", "Kavya", "Lina",
        "Mitali", "Nitika", "Pavitra", "Rupali", "Simran", "Tina", "Ujjwala", "Vijaya",
        "Yamini", "Aastha", "Bhavya", "Chhavi", "Damayanti", "Ekisha", "Fatima", "Gayathri",
        "Hema", "Ishita", "Juhi", "Kshama", "Lalita", "Madhavi", "Naina", "Priti",
        "Riya", "Shanti", "Tania", "Urvashi", "Vaidehi", "Yashaswini", "Zeenat", "Akira",
        "Bela", "Chandni", "Disha", "Esha", "Farzana", "Gul", "Harini", "Indu",
        "Janvi", "Kanta", "Lekha", "Minal", "Nupur", "Pranita", "Ruchi", "Seema",
        "Tushti", "Usha", "Vasudha", "Yukti", "Aarohi", "Bhawna", "Chhavi", "Deepti",
        "Ekta", "Falguni", "Gayatri", "Himani", "Ipsa", "Jhanvi", "Kriti", "Latika",
        "Madhumita", "Neerja", "Parineeta", "Radhika", "Saloni", "Tanisha", "Urmila",
        "Vijayalakshmi", "Yamini", "Ananya", "Bhavani", "Charulata", "Damini", "Eshaa",
        "Fatima", "Gitanjali", "Hasina", "Ila", "Juhi", "Kalyani", "Lavanya", "Madhuri",
        "Nandita", "Poonam", "Rashika", "Sai", "Shraddha", "Tara", "Uma", "Vasanti",
        "Yamini", "Zoya", "Anita", "Bela", "Chandrika", "Deepa", "Esha", "Firoza",
        "Gargi", "Hema", "Ishani", "Juhi", "Kirti", "Lata", "Meenakshi", "Nalini",
        "Pavani", "Ritika", "Sonal", "Trishna", "Ujala", "Vasudha", "Yamini", "Zara",
        "Anisha", "Bhavna", "Chandan", "Devika", "Esha", "Farah", "Gita", "Heena",
        "Indira", "Jaya", "Kavitha", "Lina", "Madhu", "Neha", "Priyanka", "Rhea",
        "Shalini", "Tanya", "Usha", "Vandita", "Yamini", "Zara"
    ]

    def unique_names(names: list[str]) -> list[str]:
        seen = set()
        unique_list = []
        for raw_name in names:
            name = raw_name.strip()
            if not name:
                continue
            lower_name = name.lower()
            if lower_name in seen:
                continue
            seen.add(lower_name)
            unique_list.append(name)
        return unique_list

    male_names = unique_names(male_names)
    female_names = unique_names(female_names)

    rows = []
    seen = set()
    for name in male_names:
        lower_name = name.lower()
        if lower_name in seen:
            continue
        seen.add(lower_name)
        rows.append((name, "male"))

    for name in female_names:
        lower_name = name.lower()
        if lower_name in seen:
            continue
        seen.add(lower_name)
        rows.append((name, "female"))

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["name", "gender"])
        for name, gender in rows:
            writer.writerow([name, gender])


if __name__ == "__main__":
    output_file = Path(__file__).resolve().parents[1] / "data" / "gender_dataset.csv"
    build_name_dataset(output_file)
    print(f"Dataset generated at: {output_file}")
