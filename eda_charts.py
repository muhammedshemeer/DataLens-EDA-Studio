import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis

def _apply_dark_theme(fig):
    fig.update_layout(
        paper_bgcolor="#0a0f1e",
        plot_bgcolor="#111827",
        font=dict(color="#e2e8f0"),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(255,255,255,0.1)", zerolinecolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(255,255,255,0.1)", zerolinecolor="rgba(255,255,255,0.1)")
    return fig

def plot_distribution(df, column):
    """Plot Histogram + KDE overlay for a numerical column."""
    try:
        clean_df = df[df[column].notna()]
        fig = ff.create_distplot([clean_df[column]], [column], show_hist=True, show_rug=False, colors=['#00d4ff'])
        fig.update_layout(title=f"Distribution of {column}")
        # Need to explicitly set the line color to purple as requested
        fig.data[1].line.color = '#7c3aed'
        return _apply_dark_theme(fig)
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=str(e), x=0.5, y=0.5, showarrow=False)
        return _apply_dark_theme(fig)

def plot_boxplot(df, column):
    """Plot box plot with outlier detection."""
    try:
        fig = px.box(df, y=column, color_discrete_sequence=['#00d4ff'])
        fig.update_traces(marker=dict(symbol='diamond', color='#ef4444', size=8))
        fig.update_layout(title=f"Box Plot of {column}")
        return _apply_dark_theme(fig)
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=str(e), x=0.5, y=0.5, showarrow=False)
        return _apply_dark_theme(fig)

def plot_bar_chart(df, column):
    """Plot horizontal bar chart for a categorical column (top 10)."""
    try:
        counts = df[column].value_counts().reset_index()
        counts.columns = [column, 'count']
        if len(counts) > 10:
            counts = counts.head(10)
        
        counts = counts.sort_values(by='count', ascending=True)
        fig = px.bar(counts, x='count', y=column, orientation='h', color='count', color_continuous_scale=['#7c3aed', '#00d4ff'])
        fig.update_layout(title=f"Top Categories in {column}")
        return _apply_dark_theme(fig)
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=str(e), x=0.5, y=0.5, showarrow=False)
        return _apply_dark_theme(fig)

def plot_correlation_heatmap(df):
    """Plot correlation heatmap for numerical columns."""
    try:
        num_cols = df.select_dtypes(include=[np.number]).columns
        corr = df[num_cols].corr()
        fig = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
        fig.update_layout(title="Correlation Heatmap")
        return _apply_dark_theme(fig)
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=str(e), x=0.5, y=0.5, showarrow=False)
        return _apply_dark_theme(fig)

def plot_pairplot(df, columns, color_col=None):
    """Plot scatter matrix (pairplot) for selected numerical columns."""
    try:
        if len(columns) > 5:
            columns = columns[:5]
            
        fig = px.scatter_matrix(df, dimensions=columns, color=color_col, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(
            title="Scatter Matrix",
            dragmode='select'
        )
        fig.update_traces(diagonal_visible=False)
        return _apply_dark_theme(fig)
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=str(e), x=0.5, y=0.5, showarrow=False)
        return _apply_dark_theme(fig)

def plot_missing_heatmap(df):
    """Plot heatmap indicating missing values."""
    try:
        missing_matrix = df.isnull().astype(int)
        fig = px.imshow(~missing_matrix.T, aspect="auto", color_continuous_scale=["#ef4444", "#10b981"])
        fig.update_layout(
            title="Missing Values Heatmap (Red=Missing, Green=Present)",
            coloraxis_showscale=False
        )
        # Hide tick labels as they can be messy with lots of rows
        fig.update_xaxes(showticklabels=False)
        return _apply_dark_theme(fig)
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=str(e), x=0.5, y=0.5, showarrow=False)
        return _apply_dark_theme(fig)

def plot_skewness_kurtosis(df):
    """Returns two figures: skewness and kurtosis bar charts."""
    try:
        num_cols = df.select_dtypes(include=[np.number]).columns
        
        skew_vals = []
        kurt_vals = []
        for col in num_cols:
            clean_col = df[col].dropna()
            if len(clean_col) > 0:
                skew_vals.append({'Column': col, 'Value': skew(clean_col)})
                kurt_vals.append({'Column': col, 'Value': kurtosis(clean_col)})
        
        skew_df = pd.DataFrame(skew_vals).sort_values(by='Value')
        kurt_df = pd.DataFrame(kurt_vals).sort_values(by='Value')
        
        # Color based on skew
        skew_colors = np.where(skew_df['Value'] > 1, '#f59e0b', 
                       np.where(skew_df['Value'] < -1, '#3b82f6', '#10b981'))
                       
        fig_skew = px.bar(skew_df, x='Value', y='Column', orientation='h')
        fig_skew.update_traces(marker_color=skew_colors)
        fig_skew.update_layout(title="Skewness")
        
        fig_kurt = px.bar(kurt_df, x='Value', y='Column', orientation='h')
        fig_kurt.update_traces(marker_color='#7c3aed')
        fig_kurt.update_layout(title="Kurtosis")
        
        return _apply_dark_theme(fig_skew), _apply_dark_theme(fig_kurt)
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=str(e), x=0.5, y=0.5, showarrow=False)
        return _apply_dark_theme(fig), _apply_dark_theme(fig)

def plot_count_plot(df, column):
    """Plot vertical bar chart for categorical counts."""
    try:
        counts = df[column].value_counts().reset_index()
        counts.columns = [column, 'count']
        fig = px.bar(counts, x=column, y='count', color='count', 
                     color_continuous_scale=['#00d4ff', '#7c3aed'], text_auto=True)
        fig.update_layout(title=f"Count Plot of {column}")
        return _apply_dark_theme(fig)
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=str(e), x=0.5, y=0.5, showarrow=False)
        return _apply_dark_theme(fig)

def plot_line_chart(df, date_col, value_col):
    """Plot line chart for time series data."""
    try:
        # Group by date if there are multiple entries per date
        temp_df = df.copy()
        temp_df[date_col] = pd.to_datetime(temp_df[date_col])
        grouped = temp_df.groupby(date_col)[value_col].mean().reset_index()
        grouped = grouped.sort_values(by=date_col)
        
        fig = px.line(grouped, x=date_col, y=value_col, markers=True)
        fig.update_traces(line=dict(color='#00d4ff'), marker=dict(color='#7c3aed', size=6))
        fig.update_layout(title=f"Trend of {value_col} over {date_col}")
        return _apply_dark_theme(fig)
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=str(e), x=0.5, y=0.5, showarrow=False)
        return _apply_dark_theme(fig)

def get_insight(df, chart_type, column=None):
    """Return an auto insight string based on the chart type."""
    try:
        if chart_type == "Distribution" and column:
            mean = df[column].mean()
            std = df[column].std()
            skewness = df[column].skew()
            if skewness > 1:
                skew_desc = "right skewed"
            elif skewness < -1:
                skew_desc = "left skewed"
            else:
                skew_desc = "normal skewed"
            return f"💡 {column}: Mean={mean:.2f} | Std={std:.2f} | Skewness={skewness:.2f} → {skew_desc}"
            
        elif chart_type == "Box Plot" and column:
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)][column]
            max_outlier = outliers.max() if len(outliers) > 0 else "None"
            return f"💡 {len(outliers)} outliers detected. IQR: [{lower_bound:.2f}, {upper_bound:.2f}]. Max outlier value: {max_outlier}"
            
        elif chart_type == "Bar Chart" and column:
            counts = df[column].value_counts()
            top_val = counts.index[0]
            top_pct = (counts.iloc[0] / len(df.dropna(subset=[column]))) * 100
            unique_vals = df[column].nunique()
            return f"💡 Most common: {top_val} ({top_pct:.1f}%). Total unique values: {unique_vals}"
            
        elif chart_type == "Correlation Heatmap":
            num_cols = df.select_dtypes(include=[np.number]).columns
            corr = df[num_cols].corr()
            # remove self correlation
            np.fill_diagonal(corr.values, np.nan)
            if corr.isna().all().all():
                 return "💡 Not enough numerical columns to find correlations."
            
            # Find max
            max_idx = corr.unstack().idxmax()
            max_val = corr.unstack()[max_idx]
            
            # Find min
            min_idx = corr.unstack().idxmin()
            min_val = corr.unstack()[min_idx]
            
            return f"💡 Strongest: {max_idx[0]} ↔ {max_idx[1]} = {max_val:.2f}. Weakest: {min_idx[0]} ↔ {min_idx[1]} = {min_val:.2f}"
            
        elif chart_type == "Pairplot" and column:
             return f"💡 {len(column)} columns selected."
             
        elif chart_type == "Missing Value Heatmap":
            missing_pct = (df.isnull().sum() / len(df)) * 100
            max_miss_col = missing_pct.idxmax()
            max_miss_val = missing_pct.max()
            total_miss = df.isnull().sum().sum()
            return f"💡 {max_miss_col} has most missing values ({max_miss_val:.1f}%). Total missing cells: {total_miss}"
            
        elif chart_type == "Skewness & Kurtosis":
            num_cols = df.select_dtypes(include=[np.number]).columns
            skew_vals = df[num_cols].skew()
            highly_skewed = sum((skew_vals > 1) | (skew_vals < -1))
            return f"💡 {highly_skewed} columns are highly skewed (>1 or <-1). Consider transformations."
            
        elif chart_type == "Count Plot" and column:
            unique_cats = df[column].nunique()
            counts = df[column].value_counts()
            top_val = counts.index[0]
            top_cnt = counts.iloc[0]
            return f"💡 {column} has {unique_cats} unique categories. Most frequent: {top_val} ({top_cnt} occurrences)"
            
        elif chart_type == "Line Plot":
            # Assuming values sorted, just a simple trend check
            return "💡 Trend analysis over time based on the selected metric."
            
        return "💡 Insight not available."
    except Exception as e:
         return f"💡 Warning: Could not generate insight ({str(e)})"
