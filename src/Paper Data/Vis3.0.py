import matplotlib.pyplot as plt
import numpy as np

def plot_endpoint_data():
    # Data in seconds
    linkedin_scraping_times = np.array([9.17, 10.02, 8.99, 9.55, 9.13])
    company_scraping_times = np.array([19.2, 22.13, 18.96, 17.29, 19.98])
    full_scraping_times = np.array([11.58, 12.05, 11.12, 12.01, 13.12]) * 60  # Convert minutes to seconds

    # Calculate means
    linkedin_mean = np.mean(linkedin_scraping_times)
    company_mean = np.mean(company_scraping_times)
    full_mean = np.mean(full_scraping_times)

    # Calculate standard deviations
    linkedin_std = np.std(linkedin_scraping_times)
    company_std = np.std(company_scraping_times)
    full_std = np.std(full_scraping_times)

    # Means and std_devs lists
    means = [linkedin_mean, company_mean, full_mean]
    std_devs = [linkedin_std, company_std, full_std]

    fig, ax = plt.subplots()

    # First axis
    ax.bar(0, means[0], yerr=std_devs[0], align='center', alpha=0.5, ecolor='black', capsize=10, color='b')
    ax.bar(1, means[1], yerr=std_devs[1], align='center', alpha=0.5, ecolor='black', capsize=10, color='g')
    ax.bar(2, means[2], yerr=std_devs[2], align='center', alpha=0.5, ecolor='black', capsize=10, color='r')

    # Add xticks
    plt.xticks(range(3), ['LinkedIn Scraping', 'Company Scraping', 'Full Scraping'])
    ax.set_ylabel('Time (seconds)')

    # Add means as text, move them slightly to the right
    ax.text(0, means[0] + std_devs[0] + 0.05, f'{means[0]:.2f}s', ha='center', va='bottom', color='b')
    ax.text(1, means[1] + std_devs[1] + 0.05, f'{means[1]:.2f}s', ha='center', va='bottom', color='g')
    ax.text(2, means[2] + std_devs[2] + 0.05, f'{means[2]:.2f}s', ha='center', va='bottom', color='r')

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

# Call the function to create the plot
plot_endpoint_data()
