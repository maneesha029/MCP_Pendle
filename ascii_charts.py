def plot_prices(history, predicted=None, title="Price Chart"):
    max_val = max(max(history), max(predicted) if predicted else max(history))
    min_val = min(min(history), min(predicted) if predicted else min(history))
    scale = 50/(max_val - min_val + 1e-6)
    print(f"\n=== {title} ===")
    for i in range(len(history)):
        hist_bar = int((history[i]-min_val)*scale)
        pred_bar = int((predicted[i]-min_val)*scale) if predicted else 0
        line = "#"*hist_bar
        if predicted: line += "|"*pred_bar
        print(line)
    print("="*60)
