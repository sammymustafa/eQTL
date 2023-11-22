from setup import *
from statsmodels.stats.multitest import multipletests
import statsmodels.api as sm

snp_data_string = eqtl_data["SnpData.txt"].decode('utf-8')
exp_data_string = eqtl_data["ExpData.txt"].decode('utf-8')

# Convert the byte strings into file-like objects
snp_data_io = StringIO(snp_data_string)
exp_data_io = StringIO(exp_data_string)

# Read the data into pandas DataFrames
snp_df = pd.read_csv(snp_data_io, sep='\t')
exp_df = pd.read_csv(exp_data_io, sep='\t')

# Subset the SNP data
snp_subset_df = snp_df.iloc[:, 222:223]

# Now proceed with eQTL analysis
# Initialize a list to store results
results = []
p_values = []

# Perform association tests for each SNP against each gene expression
for snp in snp_subset_df.columns:
    for gene in exp_df.columns[1:]:
        # Prepare the data for linear regression
        x = snp_subset_df[snp].values
        y = exp_df[gene].values
        x = sm.add_constant(x)  # Adds a constant term to the predictor

        # Perform the regression
        model = sm.OLS(y, x)
        result = model.fit()

        # Store the results and p-values for correction later
        results.append((snp, gene, result))
        p_values.append(result.pvalues[1])  # p-values[1] for the SNP coefficient

# Correct for multiple testing using FDR
rejections, pvals_corrected, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')

# Filter results for significant associations
significant_results = [(snp, gene, result) for (snp, gene, result), pval, reject in zip(results, pvals_corrected, rejections) if reject]

# Plotting for the top significant eQTLs
for i, (snp, gene, result) in enumerate(significant_results[:3]):
    plt.figure(i)
    plt.scatter(snp_subset_df[snp], exp_df[gene], alpha=0.5)
    plt.title(f'eQTL for {snp} and {gene}')
    plt.xlabel(f'Genotype for {snp}')
    plt.ylabel(f'Expression of {gene}')
    plt.plot(snp_subset_df[snp], result.predict(), color='red')  # Overlay the regression line
    plt.show()