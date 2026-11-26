import { FOOTER_HTML } from "@/content/footer";

/** The footer, rendered from the exact markup the site had before the rebuild. Do not change it. */
export default function Footer() {
  return <div className="contents" dangerouslySetInnerHTML={{ __html: FOOTER_HTML }} />;
}
