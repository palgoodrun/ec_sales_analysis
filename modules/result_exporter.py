# ==================================================
# import
# ==================================================
from pathlib import Path
import pandas as pd
import logging

# ==========================
# logger
# ==========================
logger = logging.getLogger(__name__)


# ==================================================
# export_analysis_results_to_excel
# ==================================================
def export_analysis_results_to_excel(
    output_path: Path, sheet_name_df_pairs: dict[str, pd.DataFrame]
) -> None:

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path) as writer:
        for sheet_name, df in sheet_name_df_pairs.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    logger.info(f"Excelファイル保存成功 ファイル: {output_path}")
